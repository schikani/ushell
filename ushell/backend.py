# ==========================================
# Author:    Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

from machine import reset
import network
import sys
import os


sta_if = network.WLAN(network.STA_IF)


class TerminalColors:
    color = {
        0: "\u001b[0m",     # "Reset"
        1: "\u001b[37;1m",  # "White"
        2: "\u001b[34;1m",  # "Blue"
        3: "\u001b[32;1m",  # "Green"
        4: "\u001b[31m"   # "Red"
    }



class TermHelper(TerminalColors):
    def __init__(self, username):
        super().__init__()
        self.username = username

    def pwd(self):
        return os.getcwd()

    def cd(self, dir):
        os.chdir(dir)

    def cat(self, file):
        self.head(file, 1 << 30)

    def mv(self, old, new):
        os.rename(old, new)

    def mkdir(self, dir):
        os.mkdir(dir)

    def clear(self):
        return "\x1b[2J\x1b[H"

    def ifconfig(self):
        return sta_if.ifconfig()

    def platform(self):
        return sys.platform

    def touch(self, file):
        with open(file, "w") as f:
            f.write("")
            f.close()

    def cp(self, item, loc):  # Copy file or tree
        if os.stat(item)[0] & 0x4000:  # Dir
            os.mkdir("/".join((loc, item)))
            for f in os.ilistdir(item):
                if f[0] not in ('.', '..'):
                    self.cp("/".join((item, f[0])), loc)  # File or Dir
        else:  # File
            with open(item, "r+b") as fr:
                with open("/".join((loc, item)), "w+b") as fw:
                    fw.write(fr.read())

    def rm(self, item):  # Remove file or tree
        if os.stat(item)[0] & 0x4000:  # Dir
            for f in os.ilistdir(item):
                if f[0] not in ('.', '..'):
                    self.rm("/".join((item, f[0])))  # File or Dir
            os.rmdir(item)

        else:  # File
            os.remove(item)

    def ls(self, dir=".", info=False,  helper=False):

        if helper:
            return os.listdir(dir)
        
        else:
            contents = []

            for f in os.ilistdir(dir):

                if f[1] & 0x4000 and info:
                    contents.append(self.color[2] + f[0] + self.color[0])

                elif f[1] & 0x4000 and not f[0].startswith("."):
                    contents.append(self.color[2] + f[0] + self.color[0])

                elif not f[1] & 0x4000 and info:
                    contents.append(f[0])

                elif not f[1] & 0x4000 and not f[0].startswith("."):
                    contents.append(f[0])

            contents.sort()

            return contents

    def head(self, file, lines=10):
        with open(file) as f:
            for i in range(lines):
                l = f.readline()
                if not l:
                    sys.stdout.write("\n")
                    break
                sys.stdout.write(l)

    def repl(self):
        raise EOFError

    def whoami(self):
        return self.username

    def run(self, module):
        try:
            __import__(module)
            del sys.modules[module]  # # To be able to re-import
        except KeyError:
            pass
        except ImportError:
            print(self.color[4]+"ImportError: no module named '{}'"
                  .format(module)+self.color[0])

    def reboot(self):
        reset()

