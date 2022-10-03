# ==========================================
# Copyright (c) 2021 Shivang Chikani
# Email:     shivangchikani1@gmail.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

from .logic import Logic


class Terminal(Logic):
    def __init__(self, username=None, password=None):
        super().__init__()
        self.welcome_message()
        if self.username_password(username, password, self.users):
            self.updateuser()
            self.prompt = "({0}){1}{2}@{3}{4}:{5}{6}{7}${8} "

    def whoami(self, get=False):
        if get:
            return self.username
        else:
            print(self.username)
    
    def _prompt(self):
        while True:
            env_path = self.envPath
            pwd = self.pwd(True)

            if env_path.startswith(self.userPath):
                env_path = env_path[env_path.index(self.userPath)+len(self.userPath):]
            if pwd.startswith(self.userPath):
                pwd = pwd[pwd.index(self.userPath)+len(self.userPath):]

            try:
                self._envs_data.read(self.pwd(True))
                isEnv = True
            except KeyError:
                isEnv = False

            # Set colors
            prompt = self.prompt \
                .format(env_path, self.color[3],
                        self.whoami(True), self.platform(True),
                        self.color[1], (self.color[5] if isEnv
                        else self.color[2]), pwd, self.color[1],
                        self.color[0])

            try:

                self.tokenizer(inp=input(prompt))

            except OSError as error:
                self.os_error(error)

            except KeyboardInterrupt:
                self.clear()

            except EOFError:
                break

    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self):
        self._prompt()
