# ==========================================
# Copyright (c) 2021 Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

__version__ = "1.0.2"

from .ubrainDB import ubrainDB as db
from .editor import pye
import machine
import gc
import sys
import os


try:
    import network
except ImportError:
    network = None

try:
    import upip
except ImportError:
    upip = None

class Initialize:
    def __init__(self):
        self.__version__ = __version__
        self.gc = gc
        self.gc.enable()

        self.machine = machine
        self.sys = sys
        self.os = os
        self.pye = pye
        self.network = network
        self.upip = upip

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

        self.db = db
        self.ushellDataPath = "/.ushellData"
        self._commands = self.db(self.ushellDataPath, "commands")

        try:
            self._commands.read("__ushell__")
            self.welcome_message()
        except KeyError:
            import ushell.install

        self.baseEnvPath = "/lib"
        self.envPath = self.baseEnvPath
        self.venvName = ".venv"

        self._envs_data = self.db(self.ushellDataPath, "virtualEnvs")
        self._envs_data.write(self.baseEnvPath, self.baseEnvPath)

        if self.network:
            self._networks = self.db(self.ushellDataPath, ".networks")

    def welcome_message(self):
        print("""
        {}==========================================
                    WELCOME TO USHELL
                     Version: {}
                (c) 2021 Shivang Chikani
        =========================================={}
        """.format(self.color[5], self.__version__, self.color[0]))

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
              "Your platform does not have network capabilities"
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
              "Command '{}' not found".format(cmd)
              + self.color[0])

    def not_a_valid_env(self):
        print(self.color[4] +
              "Not a valid environment. "
              "Use 'mkenv <path>' to create one."
              + self.color[0])

    def pkg_not_found(self, pkg):
        print(self.color[4] + \
              "No record found for package '{}'".format(pkg) \
              + self.color[0])

    def no_record_for_pkgs(self):
        print(self.color[4] + \
              "No record found for package/s." \
              + self.color[0])

    def os_error(self, error):
        print(self.color[4] + str(error) + self.color[0])

    def import_error(self, module):
        print(self.color[4] + "ImportError: no module named '{}'" \
              .format(module) + self.color[0])

    def too_many_args(self):
        print(self.color[4] +
              "Too many arguments"
              + self.color[0])

    def no_networks_in_database(self):
        print(self.color[4] +
              "No network/s found in database. "
              "Use 'wifiadd <ssid password>' to add one"
              + self.color[0])


class Backend(Errors):
    def __init__(self):
        super().__init__()
        self._r = "-r"
        self._a = "-a"
        self._lines = "-l"
        self._freeze = ">"
        self._undo = "-undo"
        self.__tab_size = "--tab-size"

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
        self.os.chdir(args[0])

    def cat(self, *args):
        for f in args:
            self.head(f, 1 << 30)

    def mv(self, args):
        old = args[:-1]
        new = args[-1]
        for i in old:
            self.os.rename(i, new)

    def mkdir(self, args):
        for d in args:
            self.os.mkdir(d)

    def platform(self, get=False):
        if get:
            return self.sys.platform
        else:
            print(self.sys.platform)

    def touch(self, args):

        for file in args:
            if file in (self._a or self._r):
                return self.invalid_file_name()
            with open(file, "w") as f:
                f.write("")
                f.close()

    def cp(self, args):  # Copy file or tree

        item = args[:-1]
        loc = args[-1]

        for i in item:
            if self.os.stat(i)[0] & 0x4000:  # Dir
                self.os.mkdir("/".join((loc, i)))
                for f in self.os.ilistdir(i):
                    if f[0] not in ('.', '..'):
                        self.cp(["/".join((i, f[0])), loc])  # File or Dir
            else:  # File
                with open(i, "r+b") as fr:
                    with open("/".join((loc, i)), "w+b") as fw:
                        fw.write(fr.read())

    def rm(self, args):  # Remove file or tree
        for item in args:
            if self.os.stat(item)[0] & 0x4000:  # Dir
                ifVenv = self._path_finder(item)
                try:
                    if ifVenv == self._envs_data.read(ifVenv):
                        agree = input("{}{}{} is a venv. Do you want to delete it?\n"
                                      "Type y/n: ".format(self.color[5], ifVenv, self.color[0]))
                        if agree.lower() == "y":
                            print("Removing venv: {}"
                                  .format(self.color[5] + ifVenv + self.color[0]))
                            self._envs_data.remove(ifVenv)
                            self.envPath = self.baseEnvPath
                            raise KeyError

                except KeyError:
                    for f in self.os.ilistdir(item):
                        if f[0] not in ('.', '..'):
                            self.rm(["/".join((item, f[0]))])  # File or Dir
                    try:
                        self.os.rmdir(item)
                    except OSError:
                        pass

            else:  # File
                self.os.remove(item)

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
                args = args[:-2]
                lines = args[-1]

        for file in args:
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
        pwd = self.pwd(True)
        self.cd([self.envPath])
        for module in args:

            try:
                __import__(module)
                del self.sys.modules[module]  # To be able to re-import

            except ImportError:

                self.import_error(module)

        self.cd([pwd])

    def editor(self, args):
        if len(args) == 0:
            self.pye()
        else:
            self.pye(args[0])
