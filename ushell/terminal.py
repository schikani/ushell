# ==========================================
# Copyright (c) 2021 Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

from .logic import Logic


class Terminal(Logic):
    def __init__(self, username=None):
        super().__init__()
        self.prompt = "({0}){1}{2}@{3}{4}:{5}{6}{7}${8} "
        if username:
            self.username = username
            self.user.write("user", self.username)
        else:
            if "user" in self.user.keys():
                self.username = self.user.read("user")
            
            else:
                self.username = input("Enter username for terminal: ")
                self.user.write("user", self.username)


    def whoami(self, get=False):
        if get:
            return self.username
        else:
            print(self.username)

    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self):
        while True:
            try:
                self._envs_data.read(self.pwd(True))
                isEnv = True
            except KeyError:
                isEnv = False

            # Set colors
            prompt = self.prompt \
                .format(self.envPath, self.color[3],
                        self.whoami(True), self.platform(True),
                        self.color[1], (self.color[5] if isEnv
                        else self.color[2]),self.pwd(True), self.color[1],
                        self.color[0])

            try:

                self.tokenizer(inp=input(prompt))

            except OSError as error:
                self.os_error(error)

            except KeyboardInterrupt:
                self.clear()

            except EOFError:
                break
