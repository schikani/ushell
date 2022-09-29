# ==========================================
# Copyright (c) 2021 Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

from .environment import Environment


class Logic(Environment):
    def __init__(self):
        super().__init__()
    
    def __quotes_parser(self, args):
        new_args = []
        _a = ""
        for a in args:
            if a.startswith('"') and not a.endswith('"'):
                a = a[1:]
                _a += a + " "

            elif not a.startswith('"') and a.endswith('"'):
                a = a[:-1]
                _a += a
                new_args.append(_a)
                _a = ""
            
            elif a.startswith('"') and a.endswith('"'):
                a = a[1:-1]
                new_args.append(a)

            else:
                new_args.append(a)
    
        return new_args

    def tokenizer(self, inp):

        if inp == "":
            return

        global args

        _inp = inp

        if "&&" in _inp:  # Multiple commands
            _inp = [i.split() for i in inp.split("&&")]

            for i in _inp:
                cmd = i[0]
                args = self.__quotes_parser(i[1:])
                self.execute(cmd)

        else:  # single command
            _inp = _inp.split()
            cmd = _inp[0]
            args = self.__quotes_parser(_inp[1:])
            self.execute(cmd)

    def execute(self, cmd):

        try:
            exec(self._commands.read(cmd))

        except TypeError:
            pass

        except IndexError:
            self.missing_args()

        except KeyError:
            return self.command_not_found(cmd)
