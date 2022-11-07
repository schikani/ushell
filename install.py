#!/usr/bin/python3

import os
import sys

args = sys.argv
_port_ = ""
_board_name_ = ""
_sub_mod_path_ = "submodules"

if len(args) > 1:
    _port_ = args[1]
if len(args) > 2:
    _board_name_ = args[2]
else:
    _board_name_ = "pyboard"

def submodules_update_and_upload_to_flash():
    os.system("git submodule update --init --recursive")
    submodules = os.listdir("submodules")
    rshell_upload_files(submodules)

def rshell_upload_files(submodules):
    os.system("pip3 install rshell")
    rshell_cmd = f"mkdir /{_board_name_}/lib; mkdir /{_board_name_}/lib/ushell; cp -r ./ushell/*.py /{_board_name_}/lib/ushell; "
    rshell_cmd += f"mkdir /{_board_name_}/lib/ushell_mods; cp -r ./ushell_mods/*.py /{_board_name_}/lib/ushell_mods;"
    for mod in submodules:
        rshell_cmd += f"mkdir /{_board_name_}/lib/{mod}; cp -r {_sub_mod_path_}/{mod}/*.py /{_board_name_}/lib/{mod}; "
    rshell_cmd += f"cp ush.py /{_board_name_}/lib; repl ~ from ush import *"

    os.system(f'rshell --buffer-size 8024 -p {_port_} "{rshell_cmd}"')



submodules_update_and_upload_to_flash()