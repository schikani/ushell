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


_rshell_cmds = f"mkdir /{_board_name_}/lib; cp ush.py /{_board_name_}/lib; cp -r ushell /{_board_name_}/lib; cp -r jsonDB /{_board_name_}/lib; repl ~ import machine ~ machine.reset()"

os.system(f'rshell --buffer-size 8024 -p {_port_} "{_rshell_cmds}"')