# ==========================================
# Author:    Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      7 March 2021
# Project:   ushell.ushell
# ==========================================

import sys
import os
import network

sta_if = network.WLAN(network.STA_IF)


class UShell:
    def __init__(self):
        pass

    def pwd(self):
        return os.getcwd()

    def cd(self, dir):
        return os.chdir(dir)

    def cp(self, file, loc):
        l = loc.strip("/")
        location = l + "/"

        with open(file, "r+b") as f:
            fr = f.read()

        with open(location + file, "w+b") as fw:
            fw.write(fr)

    def ls(self, dir=".", info=False):
        if info:
            l = os.listdir(dir)
            l.sort()
            for f in l:
                st = os.stat("%s/%s" % (dir, f))
                if st[0] & 0x4000:  # if a directory
                    print("   <dir> %s" % f)
                else:
                    print("% 8d %s" % (st[6], f))
        else:
            print(os.listdir(dir))

    def head(self, file, lines=10):
        with open(file) as f:
            for i in range(lines):
                l = f.readline()
                if not l:
                    break
                sys.stdout.write(l)

    def cat(self, file):
        self.head(file, 1 << 30)

    def touch(self, file):
        with open(file, "w") as f:
            f.write("")
            f.close()

    def mv(self, old, new):
        return os.rename(old, new)

    def rm(self, item):  # Remove file or tree
        if os.stat(item)[0] & 0x4000:  # Dir
            for f in os.ilistdir(item):
                if f[0] not in ('.', '..'):
                    self.rm("/".join((item, f[0])))  # File or Dir
            os.rmdir(item)
        else:  # File
            os.remove(item)

    def mkdir(self, dir):
        return os.mkdir(dir)

    def clear(self):
        return "\x1b[2J\x1b[H"

    def ifconfig(self):
        return sta_if.ifconfig()

    def platform(self):
        return sys.platform
