# ushell
### ushell is simple yet powerful Bash like terminal with an editor for devices running MicroPython (Tested on esp32 with external spiram)

## Install ushell

1. #### Clone ushell repo and change dir to ushell.
>`git clone https://github.com/schikani/ushell.git && cd ushell`

2. #### Run 'install.py' script with port and optional board name, default is 'pyboard'. It will install all the necessary files including submodules to micropython board. In the end, a status bar will be shown while installing the commands into the board and the board will reboot after the installation.
>`./install.py <port> <board_name>`

3. #### At this point you will be in the micropython repl. Simply enter the below given command. It will login the terminal with root user.
> `from ush import *`

4. #### (Optional) Run ushell at boot. After the terminal login, enter the below given command. It will append a line in 'main.py' file.
> `echo "from ush import *" >> /main.py`

## Commands
* <b>sleep</b>: Sleep for float second/s
* <b>pwd</b>: Get current working directory
* <b>cd</b>: Change directory
* <b>cp</b>: Copy file/folder to destination
* <b>head</b>: View head of file with optional '-l' param followed by no of lines
* <b>cat</b>: View entire file
* <b>touch</b>: Create file/s
* <b>mv</b>: Move file/folder from old to new location
* <b>rm</b>: Remove file/folder
* <b>mkdir</b>: Create folder
* <b>mkenv</b>: Create new virtual environment
* <b>networks</b>: List of saved networks
* <b>venvs</b>: List of virtual environments
* <b>wifiscan</b>: Scan for availale wifi networks
* <b>wificonnect</b>: Connect to any available network or to the specified network
* <b>wifiadd</b>: Add wifissid to the database
* <b>wifiremove</b>: Remove wifissid from the database
* <b>clear</b>: Clear the screen
* <b>ifconfig</b>: Network configurations (ip, gateway etc)
* <b>platform</b>: Name of the current platform
* <b>repl</b>: Read-evaluate print loop '>>>' (MicroPython prompt)
* <b>whoami</b>: Name of the user
* <b>activate</b>: Activate virtual environment
* <b>deactivate</b>: Deactivate virtual environment
* <b>reboot</b>: Reboot system
* <b>run</b>: Run micropython script
* <b>ls</b>: List current dir or specified dir
* <b>upip</b>: install/uninstall package with optional dir as '--ramdisk'
* <b>write</b>: Write to a file
* <b>users</b>: List of users
* <b>useradd</b>: Add user
* <b>userdel</b>: Delete user
* <b>login</b>: Login user
* <b>logout</b>: Logout from current user
* <b>ftp</b>: File transfer protocol (Used over wifi)
* <b>tz</b>: Set time-zone (Ex: tz 5:30)
* <b>date</b>: Get current date
* <b>echo</b>: Print to console or to a file
* <b>ping</b>: Ping to specified url/address
* <b>ushell</b>: Internal ushell interpreter, run file.ush with optional '--bg' for threaded run
* <b>gpio</b>: Gpio configuration for a pin, init/set specified pin with mode/value
* <b>passwd</b>: Set password for current user
* <b>cal</b>: Get current month calendar
* <b>help</b>: Help for all the commands