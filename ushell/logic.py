from .upipManager import UPipManager


class TermLogic(UPipManager):

    def __init__(self):
        super().__init__()

    def tokenizer(self, inp):

        _inp = inp

        try:

            if "&&" in _inp:  # Multiple commands
                _inp = [i.split() for i in inp.split("&&")]

                for i in _inp:
                    cmd = i[0]
                    args = i[1:]

                    self._token_helper(cmd, args)

            else:  # single command
                _inp = _inp.split()
                cmd = _inp[0]
                args = _inp[1:]
                self._token_helper(cmd, args)

        except IndexError as e:
            if len(_inp) == 0:
                pass
            else:
                print(self.color[4]+"Missing argument/s!"+self.color[0])

    def _token_helper(self, cmd, args):

        commands = ["pwd", "cd", "cp", "ls", "head", "cat",
                    "touch", "mv", "rm", "mkdir",
                    "clear", "ifconfig", "platform",
                    "run", "repl", "whoami", "upip",
                    "activate", "deactivate", "reboot"]

        if cmd in commands:
            if cmd == commands[0]:  # pwd
                print(self.pwd())

            elif cmd == commands[1]:  # cd
                self.cd(args[0])

            elif cmd == commands[2]:  # cp
                self.cp(args[0], args[1])

            elif cmd == commands[3]:  # ls
                if len(args) == 0:
                    for i in self.ls():
                        print(i, end="  ")
                    print("")

                elif len(args) == 1:
                    if args[0] == "-a":
                        for i in self.ls(info=True):
                            print(i, end="  ")
                        print("")
                    elif args[0] != "-a":
                        for i in self.ls(args[0]):
                            print(i, end="  ")
                        print("")

                elif len(args) == 2:
                    if args[1] == "-a":
                        for i in self.ls(args[0], info=True):
                            print(i, end="  ")
                        print("")

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
                current_dir = self.pwd()
                self.cd(self._pkg_path)
                self.run(args[0])
                self.cd(current_dir)

            elif cmd == commands[14]:  # repl
                self.repl()

            elif cmd == commands[15]:  # whoami
                print(self.whoami())

            elif cmd == commands[16]:  # upip
                if self.upip():
                    if len(args) == 2:
                        if args[0] == "install":
                            self._upip_install(package=args[1])
                        elif args[0] == "uninstall":
                            self._upip_uninstall(args[1])

                    elif len(args) == 3:
                        if args[0] == "install" and args[1] == "-r":
                            self._upip_install(package=args[2], from_file=True)

                        elif args[0] == "uninstall" and args[1] == "-r":
                            self._upip_uninstall(package=args[2], from_file=True)

                        elif args[0] == "freeze" and args[1] == ">":
                            self._upip_freeze(args[2])
                    else:
                        raise IndexError

                else:
                    print(self.color[4]+
                          "'upip' is not available for your platform"
                          +self.color[0])

            elif cmd == commands[17]:  # activate
                self._environment(path=args[0])

            elif cmd == commands[18]:  # deactivate
                self._environment(deactivate=True)

            elif cmd == commands[19]:  # reboot
                self.reboot()

        else:
            print(self.color[4]+"Command '{}' not found."
                  .format(cmd)+self.color[0])
