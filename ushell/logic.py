# ==========================================
# Copyright (c) 2022 Shivang Chikani
# Email:     shivangchikani1@gmail.com
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
        
        for index, elem in enumerate(new_args):
            if elem.startswith("$"):
                try:
                    elem = self._user_vars[self.username][elem[1:]]
                except KeyError:
                    print(self.color[4] + "'{}'".format(elem[1:]) + " variable not found!" +self.color[0])
                    return
                new_args[index] = elem
    
        return new_args
    
    def token_str_parser(self, _str):
        tokens = []
        quote_count = False
        escape = False
        _s = ""
        for s in _str:
            
            if s == '"' and not escape:
                quote_count = not quote_count

            elif s == ' ':

                if quote_count:
                    _s += s
            
                elif not quote_count:
                    tokens.append(_s)
                    _s = ""

            elif s == '$' and escape:
                _s += '\xFF\xFF\xFF'
            
            elif s == '\\':
                if not escape:
                    escape = True
                else:
                    escape = False
                    _s += s

            else:
                _s += s

            if escape and s != '\\':
                escape = False

        
        if _s:
            tokens.append(_s)
        

        for index, elem in enumerate(tokens):
            dollar_index = elem.find('$')

            if dollar_index != -1:
                for v_name, v_val in self._user_vars[self.username].items():
                    elem = elem.replace("${}".format(v_name), v_val[0])
                
                tokens[index] = elem
        
            
        return tokens


    def tokenizer(self, inp):

        inp = inp.lstrip().rstrip()

        if inp == "" or inp.startswith("#"):
            return

        global args

        _inp = inp

        if " && " in _inp:  # Multiple commands
            for i in inp.split(" && "):
                self.tokenizer(i)

        else:  # single command
            _inp = self.token_str_parser(_inp)
            cmd = _inp[0]
            args = _inp[1:]
            self.execute(cmd, args)


    def execute(self, cmd, args):

        try:
            exec(self._commands.read(cmd)[0])

        except TypeError:
            pass

        except IndexError:
            self.missing_args()

        except KeyError:
            if cmd.find("=") != -1:
                args.insert(0, cmd)
                self.add_var(args)
            
            elif cmd.startswith("$"):
                cmd = self._user_vars[self.username][cmd[1:]][0]
                self.execute(cmd, args)

            else:
                return self.command_not_found(cmd)
        
        except SyntaxError as s:
            # Giving syntax error when logout is used and logged in as root
            # Can't find the problem so not printing the error
            if cmd != "logout":
                print(self.color[4] + str(s) + ' {}'.format(cmd) + self.color[0])
