# ==========================================
# Copyright (c) 2022 Shivang Chikani
# Email:     shivangchikani1@gmail.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

__version__ = "2.1.1"

from jsonDB import jsonDB
from brain_lang import BrainLang
from .ram_block_dev import RAMBlockDev
from .cal import print_cal
from ushell_mods.uftpd import start, stop, restart
from ushell_mods.editor import pye
from ushell_mods.uping import ping
import ushell_mods.mpyaes as mpyaes
import time
import gc
import sys
import os
import machine
import random

try:
    import network
except ImportError:
    network = None

try:
    import upip
except ImportError:
    upip = None

USERS_DIR = "/.USERS"
ROOT_USERNAME = "root"
ROOT_PASSWORD = "MicroPython"

class USHELL_DEV:
    def __init__(self):
        self.__version__ = __version__
        # Colors
        self.color = {
            0: "\u001b[0m",     # "Reset"
            1: "\u001b[37;1m",  # "White"
            2: "\u001b[34;1m",  # "Blue"
            3: "\u001b[32;1m",  # "Green"
            4: "\u001b[31m",    # "Red"
            5: "\u001b[33;1m",  # "Yellow"
            6: "\u001b[36;1m",  # "Cyan"
            7: "\u001b[35;1m"   # Magenta
        }

        if ".USERS" not in os.listdir("/"):
            os.mkdir(USERS_DIR)

        self.db = jsonDB
        self.brl = BrainLang
        self.network = network
        self.ushellDataPath = "/.ushellData"
        self._commands = self.db(self.ushellDataPath, ".commands")
        self._aes = self.__init_aes__()
    
    def __init_aes__(self):

        ushell_dev_db = self.db(self.ushellDataPath, ".ushell_dev")
        if ushell_dev_db.exists("dev_key"):
            __dev_key__ = ushell_dev_db.read("dev_key", ev=True)
        else:
            seed = random.randrange(1, 10000)
            __dev_key__ = mpyaes.generate_key(16, seed)
            ushell_dev_db.write("dev_key", str(__dev_key__))
            ushell_dev_db.flush()

        return mpyaes.new(__dev_key__, mpyaes.MODE_ECB)

    def welcome_message(self):
        print("""
        {}==========================================
                    WELCOME TO USHELL
                    Version: {}
                (c) 2022 Shivang Chikani
        =========================================={}
        """.format(self.color[5], self.__version__, self.color[0]))


class Users(USHELL_DEV):
    RAM_BLOCK_DIR_PATH = "/.ramdisk"
    RAM_BLOCK_SIZE = 512 
    RAM_BLOCK_NO = 50

    def __init__(self):
        super().__init__()

        self.users = self.db(self.ushellDataPath, ".users")

        self.root_access = False
        self.username = ""
        self.userPath = ""
        self.baseEnvPath = ""
        self.envPath = ""
        self.venvName = ""
        self._envs_data = ""
        self._networks = ""
        self._user_data = ""
        self._user_vars = dict()
        self.dotUshellDirPath = ""
        self.gpio_dict = dict()

    def username_password(self, username, password, _inplace=True, _print=True):

        if ROOT_USERNAME not in self.users.keys():
            self.users.write(ROOT_USERNAME, str(self._aes.encrypt(ROOT_PASSWORD)))
            self.users.flush()

        _pass_count = 2

        while True:
            if username:
                if username in self.users.keys():
                    if not password:
                        print("Enter password for '{}' (tries left {}): ".format(username, _pass_count+1), end="")
                        password = sys.stdin.readline().strip("\n")

                    password = str(self._aes.encrypt(password))

                    if password == self.users.read(username):
                        if _print:
                            print("Login successful!")
                                # time.sleep(0.5)

                    else:
                        if _print:
                            print("Incorect password!")
                        
                        if _pass_count == 0:
                            return False

                        else:
                            _pass_count -= 1
                            password = None
                            continue


                else:
                    if _print:
                        print("No user found named '{}'".format(username))

                    if _pass_count == 0:
                        return False    

                    else:
                        _pass_count -= 1
                        username = None
                        continue

                break

            else:
                username = input("Enter ushell username (tries left {}): ".format(_pass_count+1))
                continue

        if _inplace:
            self.username = username

        return username, password

    def _set_passwd(self):
        print("Old Password: ", end="")
        old_password = sys.stdin.readline().strip("\n")
        old_password = str(self._aes.encrypt(old_password))
        if old_password == self.users.read(self.username):
            print("\nNew Password: ", end="")
            new_password = sys.stdin.readline().strip("\n")
            new_password = str(self._aes.encrypt(new_password))
            self.users.write(self.username, new_password)
            self.users.flush()
            print("New Password set!")
        else:
            print("Incorrect Old Password!")

    
    def no_permission(self):
        print(self.color[4] +
            "The user does not have the permission to do the action"
            + self.color[0])

    def user_list(self):
        for user in self.users.keys():
            print(self.color[3] + user + self.color[0])
    
    def __mk_dot_ushell(self):
        if ".ushell" not in os.listdir(self.userPath):
            os.mkdir(self.dotUshellDirPath)
        
        if "sys_vars.ush" not in os.listdir(self.dotUshellDirPath):
            user_vars = [
                'ROOT="/"\n',
                'HOME="{}"\n'.format(self.userPath),
                'BASEENV="{}"\n'.format(self.baseEnvPath),
                'RAMDISK="{}"\n'.format(self.RAM_BLOCK_DIR_PATH)
                ]
            with open(self.dotUshellDirPath+"/sys_vars.ush", "w") as sys_vars:
                for line in user_vars:
                    sys_vars.write(line)

        if "main.ush" not in os.listdir(self.dotUshellDirPath):
            with open(self.dotUshellDirPath+"/main.ush", "w") as main:
                main.write("ushell run sys_vars.ush\n")

    def updateuser(self, chdir=True, mount_ramdisk=True):
        if mount_ramdisk:
            cbdev = RAMBlockDev(512, 50)
            os.VfsLfs2.mkfs(cbdev)
            os.mount(cbdev, '{}'.format(self.RAM_BLOCK_DIR_PATH))

        if self.username != ROOT_USERNAME:
            if self.username not in os.listdir(USERS_DIR):
                os.mkdir(USERS_DIR+"/"+self.username)

        if self.username != ROOT_USERNAME:
            self.root_access = False
            self.userPath = "{}/{}".format(USERS_DIR, self.username)
            self.baseEnvPath = "{}/lib".format(self.userPath)
        else:
            self.root_access = True
            self.userPath = "/"
            self.baseEnvPath = "/lib"

        self.dotUshellDirPath = self.userPath + "/.ushell"
        
        if "lib" not in os.listdir(self.userPath):
            os.mkdir(self.baseEnvPath)

        self.envPath = self.baseEnvPath
        self.venvName = ".venv"

        self._envs_data = self.db(self.dotUshellDirPath, ".virtualEnvs")
        self._envs_data.write(self.baseEnvPath, self.baseEnvPath)
        self._envs_data.flush()

        self._user_data = self.db(self.dotUshellDirPath, ".data")
        self._user_vars[self.username] = dict()

        if self.network:
            self._networks = self.db(self.dotUshellDirPath, ".networks")
        
        self.__mk_dot_ushell()

        if chdir:
            os.chdir(self.userPath)
        

    def useradd(self, args):
        if self.root_access:
            username = args[0]
            print("Enter password for new profile" + self.color[2] + " {}".format(username) + self.color[0])
            password = sys.stdin.readline().strip("\n")
            password = str(self._aes.encrypt(password))
            self.users.write(username, password)
            self.users.flush()
            try:
                os.mkdir(USERS_DIR+"/"+username)
            except:
                pass
            print("Profile" + self.color[2] + " {} ".format(username) + self.color[0] + "created!")
            self.updateuser(chdir=False, mount_ramdisk=False)
        else:
            self.no_permission()
    
    def userdel(self, args):
        if self.root_access and args[0] != ROOT_USERNAME:
            username = args[0]
            if username in self.users.keys():
                if self.username_password(username, None, _inplace=False):
                    self.users.remove(username)
                    self.users.flush()
                    self.rm([USERS_DIR+"/"+username, "-y"])
                    print("User {} deleted successfully!".format(username))
                else:
                    print("Incorrect password!")
            else:
                print("No user named" + self.color[2] + " {} ".format(username) + self.color[0] + "found in records!")
        else:
            self.no_permission()

    def _path_parser(self, path):
        if path[0] == "~":
            userPath = self.userPath
            if userPath[-1] != "/":
                userPath += "/"
            path = userPath + path[1:]
        
        return path
    
    def rm(self, args):  # Remove file or tree
        agree = False
        if args[-1] == "-y":
            args = args[:-1]
            agree = True

        for item in args:
            item = self._path_parser(item)
            if self.os.stat(item)[0] & 0x4000:  # Dir
                ifVenv = self._path_finder(item)
                
                if ifVenv == self._envs_data.read(ifVenv):
                    if not agree:
                        agree = input("{}{}{} is a venv. Do you want to delete it?\n"
                                    "Type y/n: ".format(self.color[5], ifVenv, self.color[0]))

                        if agree.lower() == "y":
                            agree = True
                        else:
                            agree = False

                    if agree:
                        print("Removing venv: {}"
                                .format(self.color[5] + ifVenv + self.color[0]))
                        self._envs_data.remove(ifVenv)
                        self._envs_data.flush()
                        self.envPath = self.baseEnvPath
                        self.rm([item])

                else:
                    for f in self.os.ilistdir(item):
                        if f[0] not in ('.', '..'):
                            self.rm(["/".join((item, f[0]))])  # File or Dir
                    try:
                        self.os.rmdir(item)
                    except OSError:
                        pass

            else:  # File
                self.os.remove(item)

class Initialize(Users):
    def __init__(self):
        super().__init__()
        self.gc = gc
        self.gc.enable()

        self.machine = machine
        self.sys = sys
        self.os = os
        self.pye = pye
        self.upip = upip

        if not self._commands.exists("__ushell__"):
            import ushell.install


    # Progress Bar
    def progress_bar(self, iteration, total, prefix='',
                     suffix='', decimals=1, length=100,
                     fill='█', print_end="\r"):
        percent = ("{0:." + str(decimals) + "f}") \
            .format(100 * (iteration / float(total)))

        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print('\r{} {}|{}|{} {}% {}'.format(prefix, self.color[3], bar,
                                            self.color[0],
                                            percent, suffix),
              end=print_end)

        if iteration == total:
            print("")

    def reboot(self):
        self.machine.reset()


class Errors(Initialize):
    def __init__(self):
        super().__init__()


    def non_network_platform(self):
        print(self.color[4] +
              "Your platform does not have network capabilities."
              + self.color[0])

    def invalid_file_name(self):
        print(self.color[4] +
              "Invalid filename!"
              + self.color[0])

    def missing_args(self):
        print(self.color[4] +
              "Missing argument/s!"
              + self.color[0])

    def command_not_found(self, cmd):
        print(self.color[4] +
              "Command '{}' not found.".format(cmd)
              + self.color[0])

    def not_a_valid_env(self):
        print(self.color[4] +
              "Not a valid environment. "
              "Use 'mkenv <path>' to create one."
              + self.color[0])

    def pkg_not_found(self, pkg):
        print(self.color[4] +
              "No record found for package '{}'".format(pkg)
              + self.color[0])

    def no_record_for_pkgs(self):
        print(self.color[4] +
              "No record found for package/s"
              + self.color[0])

    def os_error(self, error):
        print(self.color[4] + str(error) + self.color[0])

    def import_error(self, module):
        for m in module:
            print(self.color[4] + "{}"
                .format(m) + self.color[0])

    def too_many_args(self):
        print(self.color[4] +
              "Too many arguments"
              + self.color[0])

    def no_networks_in_database(self):
        print(self.color[4] +
              "No network/s found in database. "
              "Use 'wifiadd <ssid password>' to add one"
              + self.color[0])

    def network_mentioned_not_found(self, _network):
        print(self.color[4]
              + "Network '{}' not found in database"
              .format(_network) + self.color[0])


class Backend(Errors):
    def __init__(self):
        super().__init__()
        self._r = "-r"
        self._a = "-a"
        self._lines = "-l"
        self._freeze = ">"
        self._tab = "-tab"
        self._undo = "-undo"

    def _path_finder(self, path):
        pwd = [self.pwd(True)]
        self.cd([path])
        _path = self.pwd(True)
        self.cd(pwd)
        return _path

    def clear(self):
            print("\x1b[2J\x1b[H")

    def pwd(self, get=False):
        if get:
            return self.os.getcwd()
        else:
            print(self.os.getcwd())

    def cd(self, args):
        if len(args) > 1:
            return self.too_many_args()
        self.os.chdir(self._path_parser(args[0]))

    def cat(self, *args):
        for f in args:
            self.head(self._path_parser(f), 1 << 30)

    def mv(self, args):
        old = args[:-1]
        new = args[-1]
        for i in old:
            self.os.rename(self._path_parser(i), self._path_parser(new))

    def mkdir(self, args):
        for d in args:
            self.os.mkdir(self._path_parser(d))

    def platform(self, get=False):
        if get:
            return self.sys.platform
        else:
            print(self.sys.platform)

    def touch(self, args):

        for file in args:
            if file in (self._a, self._r):
                return self.invalid_file_name()
            with open(self._path_parser(file), "w") as f:
                f.write("")
                f.close()

    def cp(self, args):  # Copy file or tree

        item = args[:-1]
        loc = self._path_parser(args[-1])

        for i in item:
            i = self._path_parser(i)
            if self.os.stat(i)[0] & 0x4000:  # Dir
                self.os.mkdir("/".join((loc, i)))
                for f in self.os.ilistdir(i):
                    if f[0] not in ('.', '..'):
                        self.cp(["/".join((i, f[0])), loc])  # File or Dir
            else:  # File
                with open(i, "r+b") as fr:
                    with open("/".join((loc, i)), "w+b") as fw:
                        fw.write(fr.read())


    def ls(self, args, helper=False):

        dirs = args
        info = None

        if len(dirs) == 0:
            dirs = [self.pwd(True)]

        elif len(dirs) == 1 and dirs[0] == self._a:
            dirs = [self.pwd(True)]
            info = self._a

        elif len(dirs) > 1 and dirs[-1] == self._a:
            dirs = dirs[:-1]
            info = self._a

        contents = []
        for index, d in enumerate(dirs):
            d = self._path_parser(d)
            if helper:
                contents = self.os.listdir(d)
                return contents

            if len(dirs) > 1:
                contents.append(("" if index == 0 else "\n")
                                + self.color[2]
                                + d + self.color[0]
                                + "=>")

            for f in self.os.ilistdir(d):

                if f[1] & 0x4000 and info == self._a:
                    contents.append(self.color[2] + f[0] + self.color[0])

                elif f[1] & 0x4000 and not f[0].startswith("."):
                    contents.append(self.color[2] + f[0] + self.color[0])

                elif not f[1] & 0x4000 and info == self._a:
                    contents.append(f[0])

                elif not f[1] & 0x4000 and not f[0].startswith("."):
                    contents.append(f[0])

        return contents

    def head(self, args, lines=10):

        if len(args) > 1:
            if args[-2] == self._lines:
                lines = int(args[-1])
                args = args[:-2]

        for file in args:
            file = self._path_parser(file)
            with open(file) as f:
                self.sys.stdout.write("\n<" +
                                      self.color[5] + file + self.color[0]
                                      + ">\n\n")
                line_n = 1
                for i in range(lines):
                    line = f.readline()
                    if not line:
                        self.sys.stdout.write("\n")
                        break
                    self.sys.stdout.write(self.color[5] +
                                          "{:02d}".format(line_n)
                                          + "\t|" + self.color[0]
                                          + line)
                    line_n += 1
                self.sys.stdout.write("\n")

    def repl(self):
        raise EOFError

    def run(self, args):
        # print(self.envPath)
        pwd = self.pwd(True)
        self.cd([self.envPath])
        for module in args:
            # print(module)
            try:
                __import__(module)
                del self.sys.modules[module]  # To be able to re-import

            except ImportError as i:
                self.import_error([i])

            except Exception as e:
                print(self.color[4]
                      + str(e) +
                      self.color[0])

        self.cd([pwd])

    def editor(self, args):
        _undo = 50
        _tab = 4
        if self._tab in args:
            _tab = int(args[args.index(self._tab) + 1])
        if self._undo in args:
            _undo = int(args[args.index(self._undo) + 1])

        if len(args) == 0:
            self.pye(undo=_undo, tab_size=_tab)
        else:
            self.pye(self._path_parser(args[0]), undo=_undo, tab_size=_tab)
    
    def ftp(self, args):
        if args[0] == "start":
            start()
        elif args[0] == "stop":
            stop()
        elif args[0] == "restart":
            restart()
    
    def ping(self, args):
        for a in args:
            ping(a)

    def set_time_zone(self, args):
        # Example tz +5:30
        _time_zone = args[0]

        hour, minutes = _time_zone.split(":")
        hour = int(hour)
        minutes = int(minutes)

        tz_offset = (hour * 3600) + (minutes * 60)

        self._user_data.write("TZ_OFFSET", tz_offset)
        self._user_data.flush()
    
    def date(self, args):

        wd = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        if self._user_data.exists("TZ_OFFSET"):
            tz_offset = self._user_data.read("TZ_OFFSET")
        else:
            tz_offset = 0
        
        year, month, month_day, hour, min, second, weekday, year_day = time.localtime(time.time() + tz_offset)
        self.sys.stdout.write("{} {}  {} {:02d}:{:02d}:{:02d} {}\n".format(wd[weekday], months[month-1], month_day, hour, min, second, year))
    
    def calendar(self):
        print_cal(self._user_data)

    
    def echo(self, args):
        if ">" not in args and ">>" not in args:
            for a in args:
                print(a, end=" ")
            print()
        
        elif len(args) > 1  and args[-2] in [">", ">>"]:
            _symbol = args[-2]
            _str_list = args[:-2]
            _str = ""
            _file_to_write = self._path_parser(args[-1])

            if _symbol == ">":
                _symbol = "w"
            
            elif _symbol == ">>":
                _symbol = "a"

            for s in _str_list:
                _str += s + " "
            _str.rstrip()

            with open(_file_to_write, _symbol) as echo_file:
                echo_file.write(_str)
                echo_file.write("\n")
    

    def add_var(self, args):
        for arg in args:

            var_name, value = arg.split("=")

            if value.startswith("$"):
                value = self._user_vars[self.username][value[1:]]

            self._user_vars[self.username][var_name] = value
    

    def _gpio(self, args):
        '''
            To control GPIO
        '''
        cmd = args[0]
        args = args[1:]

        if cmd == "init":
            pin_no = args[0]
            inp_out = args[1]
            try:
                pin_no = int(pin_no)
                inp_out = inp_out.lower()

                if inp_out == "out":
                    inp_out = machine.Pin.OUT
                elif inp_out == "in":
                    inp_out = machine.Pin.IN

                self.gpio_dict[pin_no] = machine.Pin(pin_no, inp_out)
                 

            except ValueError:
                print(self.color[4] + "Invalid pin number!" + self.color[0])
        
        elif cmd == "set":
            pin_no = args[0]
            value = args[1]

            try:
                pin_no = int(pin_no)
                value = value.lower()

                if value in ["high", "true", "1"]:
                    value = 1
                elif value in ["low", "false", "0"]:
                    value = 0

                self.gpio_dict[pin_no].value(value)
                
            except ValueError:
                print(self.color[4] + "Invalid pin number!" + self.color[0])
    
    def _sleep(self, args):
        how_long = args[0]
        try:
            how_long = float(how_long)
            time.sleep(how_long)

        except ValueError:
            pass
    

    def _help(self, args):
        if args:
            for arg in args:
                if arg in self._commands.keys():
                    print("{}".format(self._commands.read(arg)[1]))
                else:
                    print(self.color[4]+"Invalid command '{}'".format(arg)+self.color[0])
        
        else:
            for cmd, value in zip(self._commands.keys(), self._commands.values()):
                value = value[1]
                if cmd != "__ushell__":
                    print(self.color[3]+"{}".format(cmd)+self.color[0]+": "+"{}".format(value))

