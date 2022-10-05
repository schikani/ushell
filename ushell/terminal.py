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
        self.clear()
        self.welcome_message()
        if self.username_password(username, password, self.users):
            self.updateuser()
            self.prompt = "({0}){1}{2}@{3}{4}:{5}{6}{7}${8} "

    def whoami(self, get=False):
        if get:
            return self.username
        else:
            print(self.username)
    
    def _pre_prompt_script(self):

        if ".ushellrc" not in self.os.listdir("/"):
            self.touch([self.ushellrcFile])

        with open(self.ushellrcFile, "r") as ushellrc:
            for line in ushellrc:
                self.tokenizer(line.strip("\n"))
    
    def _prompt(self):

        self._pre_prompt_script()

        while True:
            env_path = self.envPath
            pwd = self.pwd(True)

            if env_path.startswith(self.userPath) and env_path != self.RAM_BLOCK_DIR_PATH+"/lib":
                env_path = env_path[env_path.index(self.userPath)+len(self.userPath):]
            if pwd.startswith(self.userPath) and not pwd.startswith(self.RAM_BLOCK_DIR_PATH):
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
