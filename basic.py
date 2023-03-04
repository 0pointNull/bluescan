import sys
import platform
import bluetooth
import threading
from argparse import ArgumentParser as AP

"""
Basic bluetooth scanner
~ v1
"""

class SimpleBluetooth:

    def __init__(self):
        pass

    @staticmethod
    def basic_scan():
        cfg = _Config()

        # How many devices were found?...
        print("\033[34m[*]\033[37m Managed to find {} devices...\033[0m".format(cfg.device_number()))

        for addr, name, dc in cfg.device():
            print(
                "\n\t\033[37m-- Device Name:\t\t\t\033[32m{}\033[0m\n"
                "\t\033[37m-- Device Address:\t\t\033[32m{}\033[0m\n"
                "\t\033[37m-- Device Class:\t\t\033[32m{}\033[0m\n\n".format(name, addr, dc)
            )

    @staticmethod
    def add_service_scan():
        print("\033[34m[*]\033[37m Managed to find {} devices...\033[0m".format(_Config.basic_device_setup_list()))

        for addr, name in _Config.basic_device_setup():
            print("\t\033[37mFor Name:\t\t\033[33m{}\033[0m\n"
                  "\t\033[37mFor Address:\t\t\033[33m{}\033[0m".format(name, addr))

            # Init service module
            srv = bluetooth.find_service(address=addr)

            if len(srv) == 0:
                print("\t\033[31mNo services found for device...\033[0m\n")
            else:
                print("\t\033[37mService(s) found:\n\t\033[33m{}\033[0m\n\n".format(srv))
            continue


class _Config:

    def __init__(self):
        self.devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
        self.devno = len(self.devices)

    def device(self):
        return self.devices

    def device_number(self):
        return self.devno

    @staticmethod
    def basic_device_setup():
        device = bluetooth.discover_devices(duration=5, lookup_names=True)

        return device

    @staticmethod
    def basic_device_setup_list():
        device = bluetooth.discover_devices(duration=5, lookup_names=True)
        devno = len(device)

        return devno

    @staticmethod
    def get_version():
        return "v1.0 -- m1"

    @staticmethod
    def check_os():
        if platform.system() == "win32":
            print("Please run on Linux..."); exit(1)


def main():
    _Config.check_os()

    ops = AP(usage="blues.py [OPTIONS] | -h, --help", conflict_handler="resolve")

    ops.add_argument('-v', '--version', action="store_true", dest="get_version", help="Print module version and exit")
    ops.add_argument('-b', '--basic', action="store_true", dest="init_basic_scan", help="Initialize a basic bluetooth scan")
    ops.add_argument('-s', '--service-scan', action="store_true", dest="add_service_scan", help="Add service scanning to bluetooth scan")

    args = ops.parse_args()

    if args.get_version:
        print("\n\033[37m++ Module Version: {}\033[0m\n".format(_Config.get_version()))

    if args.init_basic_scan:
        print("\033[32m[+]\033[37m Running basic bluetooth scanner...\033[0m")

        t = threading.Thread(target=SimpleBluetooth.basic_scan(), args=(1,))
        t.start()

    if args.add_service_scan:
        print("\033[32m[+]\033[37m Running service scanner...\033[0m")

        t = threading.Thread(target=SimpleBluetooth.add_service_scan(), args=(1,))
        t.start()

main()