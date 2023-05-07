# ==========================================
# Copyright (c) 2022 Shivang Chikani
# Email:     shivangchikani1@gmail.com
# Date:      7 March 2021
# Project:   ushell
# ==========================================
    
from .backend import Backend
import ntptime


class Environment(Backend):
    def __init__(self):
        super().__init__()

    def _venv(self, path):
        return self.db(path, self.venvName)

    def _upip_install_helper(self, package_dict, package, envPath=None):
        if not envPath:
            envPath = self.envPath
        _contents_before = set(self.ls([envPath], helper=True))
        self.mip.install(package, envPath)
        _contents_after = set(self.ls([envPath], helper=True))
        _package_files = list(_contents_before.symmetric_difference(_contents_after))

        if len(_package_files) > 0:
            package_dict.update({package: _package_files})
            return package_dict

    def ifconfig(self, get=False):
        if self.network:
            sta_if = self.network.WLAN(self.network.STA_IF)
            if get:
                return sta_if.ifconfig()
            else:
                print(sta_if.ifconfig())
        else:
            return self.non_network_platform()

    def add_network(self, args):
        ssid = args[0]
        print("Enter password for network " + self.color[2] + "{}".format(ssid) + self.color[0])
        password = self.sys.stdin.readline().strip("\n")
        password = str(self._aes.encrypt(password.encode()))

        if self.network:
            self._networks.write(ssid, password)
            self._networks.flush()
            print("Network {} added successfully."
                  .format(self.color[6] + ssid + self.color[0]))

        else:
            return self.non_network_platform()

    def remove_network(self, args):
        if self.network:
            for network in args:
                try:
                    self._networks.remove(network)
                    self._networks.flush()
                    print("Network {} removed successfully."
                        .format(self.color[6] + network + self.color[0]))

                except KeyError:
                    return self.network_mentioned_not_found(network)
        else:
            return self.non_network_platform()

    def wifi_scan(self):
        if self.network:
            sta_if = self.network.WLAN(self.network.STA_IF)
            sta_if.active(True)
            counter = 1
            scanned = sta_if.scan()
            for netw in scanned:
                print("[{}] ".format(counter)
                    + self.color[6]
                    + netw[0].decode('utf-8')
                    + self.color[0], end="  ")
                print("")
                counter += 1
            try:
                index = int(input("Enter index number to add a network: "))
                index -= 1
                if index > -1 and index < len(scanned)-1:
                    self.add_network([scanned[index][0].decode('utf-8')])
            except ValueError:
                pass

        else:
            return self.non_network_platform()

    def scan_and_connect(self, args=None):
        if self.network:
            if len(self._networks.keys()) > 0:
                found = self.color[6] + "{}" + self.color[0]
                sta_if = self.network.WLAN(self.network.STA_IF)
                if not sta_if.isconnected() or args:
                    # Get keys and values as bytes objects in a dictionary
                    dict_B = self._networks.items()
                    sta_if.active(True)
                    if not args:
                        print('Scanning for available networks ...')
                        for netw in sta_if.scan():
                            netw = netw[0].decode('utf-8')
                            # catch ssid from index 0 and
                            # compare it with the dictionary keys
                            if netw in dict_B.keys():
                                found = found.format(netw)
                                print("found: {}".format(found))
                                sta_if.connect(netw, self._aes.decrypt(eval(dict_B[netw])).decode("utf-8"))
                                break
                            else:
                                return self.no_networks_in_database()
                    else:
                        sta_if.active(False)
                        sta_if.active(True)
                        ssid = args[0]
                        if ssid in dict_B.keys():
                            found = found.format(ssid)
                            print('Connecting to network: {}'.format(found))
                            sta_if.connect(ssid, self._aes.decrypt(eval(dict_B[ssid])).decode("utf-8"))
                        else:
                            return self.network_mentioned_not_found(ssid)
                    while not sta_if.isconnected():
                        pass
                    ntptime.settime()
                    print('network config:', sta_if.ifconfig())

                else:
                    ntptime.settime()
                    print("network config:", end=" "), self.ifconfig()
            else:
                return self.no_networks_in_database()
        else:
            return self.non_network_platform()

    def networks(self):
        if self.network:
            networks = self._networks.keys()
            networks = ['"'+self.color[6] + net + self.color[0]+'"' for net in networks]
            return networks
        else:
            return self.non_network_platform()

    def venvs(self):
        envs = self._envs_data.keys()
        envs = ['"'+self.color[5] + venv + self.color[0]+'"' for venv in envs]
        return envs

    def mkenv(self, args):
        paths = args
        for path in paths:
            try:
                self.mkdir([path])
            except OSError:
                pass
            _path = self._path_finder(path)
            self._venv(_path)
            self._envs_data.write(_path, _path)
            self._envs_data.flush()

    def environment(self, *args):
        if args[0] == 'activate':
            path = args[1][0]
            _path = self._path_finder(path)
            try:
                self.envPath = self._envs_data.read(_path)
            except KeyError:
                return self.not_a_valid_env()

        elif args[0] == 'deactivate':
            self.envPath = self.baseEnvPath

    def mip_manager(self, args):

        if self.mip:
            ramdisk = True if args[-1] == "--ramdisk" else False
            if ramdisk:
                self.envPath = self.RAM_BLOCK_DIR_PATH+"/lib"
                args = args[:-1]

            venv = self._venv(self.envPath)
            action = args[0]
            package = args[1:]
            symbol = None

            if package[0] in (self._r, self._freeze):
                symbol = package[0]
                package = package[1:]

            for _pkg in package:

                # upip install

                if action == "install":

                    package_dict = {}

                    if symbol == self._r:
                        with open(_pkg, "r") as fr:
                            while True:
                                pkg = fr.readline().strip("\n")
                                if not pkg:
                                    break
                                package_names = self._upip_install_helper(package_dict, pkg)

                    else:
                        package_names = self._upip_install_helper(package_dict, _pkg)

                    if package_names:
                        for key, value in package_names.items():
                            venv.write(key, value)

                # upip uninstall

                elif action == "uninstall":

                    if symbol == self._r:
                        with open(_pkg, "r") as fr:
                            while True:
                                pkg = fr.readline().strip("\n")
                                if not pkg:
                                    break
                                self.mip_manager(["uninstall", pkg])
                    else:

                        try:
                            for i in venv.read(_pkg):
                                self.rm(["/".join((self.envPath, i))])
                            venv.remove(_pkg)
                            print("Package '{}' removed".format(_pkg))

                        except KeyError:
                            return self.pkg_not_found(_pkg)

                # upip freeze

                elif action == "freeze":

                    if symbol == self._freeze:
                        packages = venv.keys()

                        if len(packages) > 0:
                            with open(_pkg, "w") as fzw:
                                for k in packages:
                                    fzw.write(k + "\n")
                        else:
                            return self.no_record_for_pkgs()

            venv.flush()

        else:
            print("mip not installed in system!")
            return None
            # return self.non_network_platform()
