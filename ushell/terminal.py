# ==========================================
# Author:    Shivang Chikani
# Email:     mail@shivangchikani.com
# Date:      12 March 2021
# Project:   ushell
# ==========================================


from .logic import TermLogic


class Terminal(TermLogic):

    def __init__(self, username):
        self.prompt = "({0}){1}{2}@{3}{4}:{5}{6}{7}${8} "
        self.username = username
        super().__init__()

    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self):

        while True:

            # Set colors
            prompt = self.prompt \
                .format(self._pkg_path, self.color[3],
                        self.whoami(), self.platform(),
                        self.color[1], self.color[2],
                        self.pwd(), self.color[1], self.color[0])

            try:

                self.tokenizer(inp=input(prompt))

            except OSError as error:
                print(self.color[4]+str(error)+self.color[0])

            except EOFError:
                break

            except KeyboardInterrupt:
                print(self.clear())

    # def help(self):
    #     help_ = """
    #     UShell
    #     ```````````````````
    #     COMMAND <:> USAGE
    #     <:> DESCRIPTION
    #     ```````````````````
    #     "pwd" <:> pwd
    #     <:> Get current working directory\n
    #     "cd" <:> cd dir
    #     <:> Change directory to specified directory\n
    #     "cp" <:> cp file.py folder ; cp folder folder1
    #     <:> Copy file or folder to specified location\n
    #     "ls" <:> ls dir ; ls dir -i
    #     <:> Get directory contents.\n\tOptionally get more details with -i\n
    #     ``````````````````
    #     """
