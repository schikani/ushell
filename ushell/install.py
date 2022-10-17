# ==========================================
# Copyright (c) 2022 Shivang Chikani
# Email:     shivangchikani1@gmail.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================

from .backend import Initialize

init = Initialize()
db = init._commands

COMMANDS = {
    "__ushell__": [True,""],

    "sleep": ["terminal._sleep(args)", "Sleep for float second/s"],

    "pwd": ["terminal.pwd()", "Get current working directory"],

    "cd": ["terminal.cd(args)", "Change directory to <dir>"],

    "cp": ["terminal.cp(args)", "Copy <src> to <dest>"],

    "head": ["terminal.head(args)", "View head of <file> with optional '-l' <no_of_line>"],

    "cat": ["terminal.cat(args)", "View entire <file>"],

    "touch": ["terminal.touch(args)", "Create <file>"],

    "mv": ["terminal.mv(args)", "Move from <old> to <new> location"],

    "rm": ["terminal.rm(args)", "Remove <dir or file>"],

    "mkdir": ["terminal.mkdir(args)", "Create <dir>"],

    "mkenv": ["terminal.mkenv(args)", "Create <virtualenv>"],

    "networks": ["[print(x, end='  ') for x in terminal.networks()];print('')", "List of saved networks"],

    "venvs": ["[print(x, end='  ') for x in terminal.venvs()];print('')", "List of virtual environments"],

    "wifiscan": ["terminal.wifi_scan()", "Scan for availale wifi networks"],

    "wificonnect": ["terminal.scan_and_connect(args)", "Connect to any available network or to <specified network>"],

    "wifiadd": ["terminal.add_network(args)", "Add <wifissid> to database"],

    "wifiremove": ["terminal.remove_network(args)", "Remove <wifissid> from database"],

    "clear": ["terminal.clear()", "Clear the screen"],

    "ifconfig": ["terminal.ifconfig()", "Network configurations (ip, gateway etc)"],

    "platform": ["terminal.platform()", "Name of the current platform"],

    "repl": ["terminal.repl()", "Read-evaluate print loop '>>>' (MicroPython prompt)"],

    "whoami": ["terminal.whoami()", "Name of user"],

    "activate": ["terminal.environment('activate', args)", "Activate <virtualenv>"],

    "deactivate": ["terminal.environment('deactivate')", "Deactivate virtualenv"],

    "reboot": ["terminal.reboot()", "Reboot system"],

    "run": ["terminal.run(args)", "Run <python script>"],

    "ls": ["[print(x, end='  ') for x in terminal.ls(args)];print()", "List current dir or <specified dir>"],

    # upip
    "upip": ["terminal.upip_manager(args)", "<install/uninstall> <package> with optional dir as '--ramdisk'"],

    # Micropython-Editor
    "write": ["terminal.editor(args)", "Write <to a file>"],

    # Users
    "users": ["terminal.user_list()", "List of users"],

    # Add user
    "useradd": ["terminal.useradd(args)", "Add <username>"],

    # Delete user
    "userdel": ["terminal.userdel(args)", "Delete <username>"],

    # Login
    "login": ["terminal.login(args)", "Login <username>"],
    
    # Logout
    "logout": ["terminal.logout()", "Logout from current user"],

    # Ftp
    "ftp": ["terminal.ftp(args)", "File transfer protocol (Used over wifi)"],

    # Set-time-zone
    # Example: tz +5:30
    "tz": ["terminal.set_time_zone(args)", "Set <time-zone>"],

    # Get current date
    "date": ["terminal.date(args)", "Get current date"],

    # Echo
    # Example: echo "Hello World!", echo "Hello World!" >> new.txt
    "echo": ["terminal.echo(args)", "Print to console or to <file>"],

    #Ping
    "ping": ["terminal.ping(args)", "Ping <to specified url/address>"],

    # Ushell (run)
    "ushell": ["terminal._ushell(args)", "Internal ushell interpreter, run <file.ush> as optional '--bg' for threaded run"],

    # GPIO
    "gpio": ["terminal._gpio(args)", "Gpio configuration for a pin, init/set <specified pin> <mode/value>"],

    "help": ["terminal._help(args)", "Help for all the commands"]
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

