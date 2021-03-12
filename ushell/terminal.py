# ==========================================
# Author:    Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      12 March 2021
# Project:   ushell.terminal
# ==========================================


from .ushell import UShell
from machine import reset
import sys


class Terminal(UShell):

    def __init__(self, user):
        self.user = user
        super().__init__()

    def __repr__(self):
        self.__call__()
        return ""

    def __helper__(self, cmd, args):
        commands = ["pwd", "cd", "cp", "ls", "head", "cat",
                    "touch", "mv", "rm", "mkdir",
                    "clear", "ifconfig", "platform",
                    "run", "repl", "whoami", "reboot"]

        if cmd in commands:
            if cmd == commands[0]:  # pwd
                print(self.pwd())

            elif cmd == commands[1]:  # cd
                self.cd(args[0])

            elif cmd == commands[2]:  # cp
                self.cp(args[0], args[1])

            elif cmd == commands[3] and len(args) == 0:  # ls
                self.ls()

            elif cmd == commands[3] and len(args) == 1 and args[0] != "-i":
                self.ls(args[0])

            elif cmd == commands[3] and len(args) == 1 and args[0] == "-i":
                self.ls(info=True)

            elif cmd == commands[3] and len(args) == 2 and args[1] == "-i":
                self.ls(args[0], info=True)

            elif cmd == commands[4] and len(args) == 1:  # head
                self.head(args[0])

            elif cmd == commands[4] and len(args) == 2:
                self.head(args[0], lines=int(args[1]))

            elif cmd == commands[5]:  # cat
                self.cat(args[0])

            elif cmd == commands[6]:  # touch
                self.touch(args[0])

            elif cmd == commands[7]:  # mv
                self.mv(args[0], args[1])

            elif cmd == commands[8]:  # rm
                self.rm(args[0])

            elif cmd == commands[9]:  # mkdir
                self.mkdir(args[0])

            elif cmd == commands[10]:  # clear
                print(self.clear())

            elif cmd == commands[11]:  # ifconfig
                print(self.ifconfig())

            elif cmd == commands[12]:  # platform
                print(self.platform())

            elif cmd == commands[13]:  # run
                try:
                    __import__(args[0])
                    del sys.modules[args[0]]  # # To be able to re-import
                except KeyError:
                    pass
                except ImportError:
                    print("ImportError: no module named '{}'".format(args[0]))

            elif cmd == commands[14]:  # repl
                raise KeyboardInterrupt

            elif cmd == commands[15]:  # whoami
                print(self.user)

            elif cmd == commands[16]:  # reboot
                reset()

        else:
            print("Command '{}' not found.".format(cmd))

    def __call__(self):

        # Font Colours
        fcolor = {
            0: "\u001b[32;1m",  # "Green"
            1: "\u001b[34;1m",  # "Blue"
            2: "\u001b[37;1m",  # "White"
            3: "\u001b[0m"      # "Reset"
        }
        while True:

            prompt = "{0}{1}@{2}{3}:{4}{5}{6}${7} " \
                .format(fcolor[0], self.user, self.platform(), fcolor[2], fcolor[1], self.pwd(), fcolor[2], fcolor[3])

            try:

                inp = input(prompt)

                if "&&" in inp:  # Multiple commands
                    inp = [i.split() for i in inp.split("&&")]

                    for i in inp:
                        cmd = i[0]
                        args = i[1:]

                        self.__helper__(cmd, args)

                else:  # single command
                    inp = inp.split()
                    cmd = inp[0]
                    args = inp[1:]
                    self.__helper__(cmd, args)

            except IndexError as e:
                print(e)

            except OSError as e:
                print(e)

            except EOFError:
                print(self.clear())

            except KeyboardInterrupt:
                break
