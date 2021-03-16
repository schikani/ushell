from .backend import TermHelper
import json

try:
    import upip

except ImportError:
    upip = False


class UPipManager(TermHelper):
    def __init__(self):
        super().__init__(username=self.username)
        self._pkg_path = "/lib"
        self._pkg_record_path = "/lib/.record.json"

    def upip(self):
        return upip

    def _environment(self, path=None, deactivate=False):

        if path:
            self._pkg_path = path
            self._pkg_record_path = "/".join((path, ".record.json"))

        elif deactivate:
            self._pkg_path = "/lib"
            self._pkg_record_path = "/lib/.record.json"

        try:
            self.mkdir(self._pkg_path)
        except OSError:
            pass


    def _upip_install_helper(self, package_dict, package):
        _contents_before = set(self.ls(dir=self._pkg_path, helper=True))
        self.upip().install(package, self._pkg_path)
        _contents_after = set(self.ls(dir=self._pkg_path, helper=True))
        _package_files = list(_contents_before.symmetric_difference(_contents_after))
        if len(_package_files) > 0:
            package_dict.update({package: _package_files})
            return package_dict

    def _upip_install(self, package, from_file=False):
        package_dict = {}

        if from_file:
            with open(package, "r") as fr:
                while True:
                    pkg = fr.readline().strip("\n")
                    if not pkg:
                        break
                    package_names = self._upip_install_helper(package_dict, pkg)

        else:
            package_names = self._upip_install_helper(package_dict, package)

        try:
            with open(self._pkg_record_path, "r") as jfr:
                jfr = json.load(jfr)
                jfr.update(package_names)
            with open(self._pkg_record_path, "w") as jfw:
                json.dump(jfr, jfw)
        except:
            with open(self._pkg_record_path, "w") as jfw:
                json.dump(package_names, jfw)

    def _upip_uninstall(self, package, from_file=False):
        if from_file:
            with open(package, "r") as fr:
                while True:
                    pkg = fr.readline().strip("\n")
                    if not pkg:
                        break
                    self._upip_uninstall(package=pkg)
        else:

            try:
                with open(self._pkg_record_path, "r") as jfr:
                    jfr = json.load(jfr)

                for i in self.ls(self._pkg_path, helper=True):
                    if i in jfr[package]:
                        self.rm("/".join((self._pkg_path, i)))
                del jfr[package]
                with open(self._pkg_record_path, "w") as jfw:
                    json.dump(jfr, jfw)

                print("Package '{}' removed".format(package))

            except:
                print(self.color[4]+
                      "No record found for package '{}'".format(package)
                      +self.color[0])

    def _upip_freeze(self, path):
        try:
            with open(self._pkg_record_path, "r") as jfr:
                jfr = json.load(jfr)
            with open(path, "w") as fzw:
                for k in jfr.keys():
                    fzw.write(k + "\n")
        except:
            print(self.color[4]+
                  "No record found for package/s."
                  +self.color[0])
