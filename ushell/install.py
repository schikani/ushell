# ==========================================
# Copyright (c) 2021 Shivang Chikani
# Email:     shivangchikani1@gmail.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

from .backend import Initialize

init = Initialize()
db = init._commands

COMMANDS = {
    "__ushell__": True,

    "pwd": "terminal.pwd()",

    "cd": "terminal.cd(args)",

    "cp": "terminal.cp(args)",

    "head": "terminal.head(args)",

    "cat": "terminal.cat(args)",

    "touch": "terminal.touch(args)",

    "mv": "terminal.mv(args)",

    "rm": "terminal.rm(args)",

    "mkdir": "terminal.mkdir(args)",

    "mkenv": "terminal.mkenv(args)",

    "networks": "[print(x, end='  ') for x in terminal.networks()];print('')",

    "venvs": "[print(x, end='  ') for x in terminal.venvs()];print('')",

    "wifiscan": "terminal.wifi_scan()",

    "wificonnect": "terminal.scan_and_connect(args)",

    "wifiadd": "terminal.add_network(args)",

    "wifiremove": "terminal.remove_network(args)",

    "clear": "terminal.clear()",

    "ifconfig": "terminal.ifconfig()",

    "platform": "terminal.platform()",

    "repl": "terminal.repl()",

    "whoami": "terminal.whoami()",

    "activate": "terminal.environment('activate', args)",

    "deactivate": "terminal.environment('deactivate')",

    "reboot": "terminal.reboot()",

    "run": "terminal.run(args)",

    "ls": "[print(x, end='  ') for x in terminal.ls(args)];print()",

    # upip
    "upip": "terminal.upip_manager(args)",

    # Micropython-Editor
    "write": "terminal.editor(args)",

    # Users
    "users": "terminal.user_list()",

    # Add user
    "useradd": "terminal.useradd(args)",

    # Delete user
    "userdel": "terminal.userdel(args)",

    # Login
    "login": "terminal.login(args)",
    
    # Logout
    "logout": "terminal.logout()",
}


def install(dict, db, prefix):
    dict_len = len(dict)
    init.progress_bar(0, total=dict_len, prefix=prefix, suffix='Complete', length=50)

    for index, (key, value) in enumerate(dict.items()):
        db.write(key, value)
        init.progress_bar(index + 1, total=dict_len, prefix=prefix, suffix='Complete', length=50)

    print("The System will now reboot")
    db.close()
    init.reboot()


# Install Commands
install(dict=COMMANDS, db=db, prefix=' Updating ushell commands:')

