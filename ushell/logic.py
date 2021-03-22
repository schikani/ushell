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

    def tokenizer(self, inp):

        if inp == "":
            return

        global args
        cmd = ""

        _inp = inp

        if "&&" in _inp:  # Multiple commands
            _inp = [i.split() for i in inp.split("&&")]

            for i in _inp:
                cmd = i[0]
                args = i[1:]
                self.execute(cmd)

        else:  # single command
            _inp = _inp.split()
            cmd = _inp[0]
            args = _inp[1:]
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
