#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface whose MAC address is to be changed")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify the interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify the new mac, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address of " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if not mac_address_search_result.group(0):
        print("[-] Could not read the MAC address of the specified interface")
    else:
        return mac_address_search_result.group(0)


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[.] Current MAC = " + str(current_mac))


change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address successfully changed to " + options.new_mac)
else:
    print("[-] Unable to change the MAC Address to the specified value")
