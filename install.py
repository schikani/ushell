#!/usr/bin/python3

import os
import sys

args = sys.argv
_port_ = ""
_board_name_ = ""

if len(args) > 1:
    _port_ = args[1]
if len(args) > 2:
    _board_name_ = args[2]
else:
    _board_name_ = "pyboard"

def submodules_update():
    os.system("git submodule update --init --recursive")


def rshell_upload_files():
    os.system("pip3 install rshell")
    rshell_mkdir = f"mkdir /{_board_name_}/lib; mkdir /{_board_name_}/lib/ushell; mkdir /{_board_name_}/lib/jsonDB; mkdir /{_board_name_}/lib/brain_lang"
    rshell_cp_files = f"cp -r ./ushell/*.py /{_board_name_}/lib/ushell; cp -r ./jsonDB/*.py /{_board_name_}/lib/jsonDB; cp -r ./brain_lang/*.py /{_board_name_}/lib/brain_lang; cp ush.py /{_board_name_}"
    rshell_repl_cmds = f"repl ~ from ush import *"
    rshell_all_cmds = f"{rshell_mkdir}; {rshell_cp_files}; {rshell_repl_cmds}"
    os.system(f'rshell --buffer-size 8024 -p {_port_} "{rshell_all_cmds}"')



submodules_update()
rshell_upload_files()