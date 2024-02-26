# Copyright 2019-2024 Peppy Player peppy.player@gmail.com
#
# This file is part of Peppy Player.
#
# Peppy Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peppy Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peppy Player. If not, see <http://www.gnu.org/licenses/>.

import sys
import subprocess
import logging
import json

from ui.state import State
from util.config import COLORS, COLOR_DARK

MENU_ROWS_WIFI = 5
MENU_COLUMNS_WIFI = 2
PAGE_SIZE_WIFI = MENU_ROWS_WIFI * MENU_COLUMNS_WIFI

WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"

CONNECTED = "connected"
ETHERNET_IP = "ethernet IP"
WIFI_NETWORK = "wi-fi network name"
WIFI_IP = "wi-fi IP"

class WiFiUtil(object):
    """ WiFi Utility class """

    def __init__(self, util):
        """ Initializer

        :param util: utility object
        """
        self.util = util
        self.config = util.config
        self.image_util = util.image_util

    def get_network(self):
        """ Get network info

        :return: network info
        """
        if "win" in sys.platform:
            return self.get_windows_network()
        else:
            return self.get_linux_network()

    def get_windows_network(self):
        """ Get Windows network info

        :return: network info
        """
        n = subprocess.check_output("ipconfig")
        lines = n.decode("utf8").split("\n")
        result = {}
        found_eth = False
        found_wifi = False
        for line in lines:
            if not found_eth and "Ethernet adapter Ethernet:" in line:
                found_eth = True
                found_wifi = False
            elif not found_eth and "Wireless LAN adapter Wi-Fi:" in line:
                found_wifi = True
                found_eth = False

            if found_eth and "IPv4 Address" in line:
                result[ETHERNET_IP] = line.split(":")[-1].strip()
                found_eth = False
            if found_wifi and "IPv4 Address" in line:
                result[WIFI_IP] = line.split(":")[-1].strip()
                found_wifi = False

        info = self.get_windows_wifi_info()
        try:
            result[WIFI_NETWORK] = info["profile"]
        except:
            pass

        return result

    def get_linux_network(self):
        """ Get Linux network info using 'ip' utility.
        If there many entries of the same type (eth or wlan) the function returns the last one.

        :return: network info
        """
        result = {}
        n = subprocess.check_output(["ip", "-j", "a"])
        js = json.loads(n)

        for e in js:
            try:
                e["addr_info"]
            except:
                continue # if no addr_info

            inet_addr = None
            try:
                for a in e["addr_info"]:
                    if a["family"] == "inet":
                        inet_addr = a["local"]
                        break
            except:
                pass

            if e["ifname"].startswith("e") and inet_addr:
                result[ETHERNET_IP] = inet_addr
            elif e["ifname"].startswith("w") and inet_addr:
                result[WIFI_IP] = inet_addr

        logging.debug("Get wifi info...")
        info = self.get_linux_networks()
        try:
            result[WIFI_NETWORK] = info["profile"]
        except:
            pass

        logging.debug(f"Linux network complete info: {result}")

        return result

    def get_wifi_networks(self):
        """ Get Wi-Fi networks

        :return: wi-fi networks
        """
        if "win" in sys.platform:
            return self.get_windows_wifi_info()
        else:
            return self.get_linux_networks()

    def get_page_num(self, network, networks):
        """ Get Wi-Fi page number for the provided network

        :param network: given Wi-Fi network
        :param networks: all networks

        :return: page number for specified network
        """
        try:
            networks[network]
        except:
            return 1

        i = networks[network].index
        n = int(i / PAGE_SIZE_WIFI)
        r = int(i % PAGE_SIZE_WIFI)
        if r > 0:
            n += 1

        return n

    def get_network_page(self, page, networks):
        """ Get page of networks for provided page number

        :param page: page number
        :param networks: list of networks

        :return: page of networks
        """
        p = {}
        if len(networks) == 0:
            return p

        start_index = (page - 1) * PAGE_SIZE_WIFI
        end_index = start_index + PAGE_SIZE_WIFI

        for k, v in networks.items():
            if v.index >= start_index and v.index < end_index:
                p[k] = v

        return p

    def get_network_info(self, index, name, strength, bb):
        """ Prepare state object for network button

        :param index: network index
        :param name: network name
        :param strength: signal strength
        :param bb: bounding box
        :return: state object with network info
        """
        s = State()
        s.index = index
        s.name = name
        s.l_name = name
        s.strength = strength
        s.comparator_item = s.index
        s.bgr = self.config[COLORS][COLOR_DARK]
        s.show_bgr = True

        if strength <= 25:
            n = "s-1"
        elif strength > 25 and strength <= 50:
            n = "s-2"
        elif strength > 50 and strength <= 75:
            n = "s-3"
        elif strength > 75:
            n = "s-4"

        s.icon_base = self.image_util.load_icon_main(n, bb, 0.5)

        return s

    def get_windows_wifi_info(self):
        """ Collect Windows Wi-Fi info

        :return: wi-fi info
        """
        wifi_info = {}
        networks = []
        start = "SHOW NETWORKS MODE=BSSID"
        end = "SHOW INTERFACE CAPABILITIES"
        n = subprocess.check_output(["netsh", "wlan", "show", "all"])
        d = n.decode("utf8")
        start_index = d.find(start)
        end_index = d.find(end)
        sub = d[start_index: end_index]

        if len(sub) == 0:
            return networks

        found_name = False
        lines = sub.split("\n")
        network_name = None
        for line in lines:
            if line.startswith("SSID"):
                name_start = line.index(":") + 1
                name = line[name_start:].strip()
                if len(name) > 0:
                    found_name = True
                    network_name = name
            else:
                if "Signal" in line and found_name:
                    signal_start = line.index(":") + 1
                    network_signal = line[signal_start:].strip()
                    networks.append({"name": network_name, "strength": int(network_signal[:-1])})
                    found_name = False

        wifi_info["networks"] = networks

        start_index = d.find("User profiles")
        sub = d[start_index:]
        lines = sub.split("\n")
        for line in lines:
            if "All User Profile" in line:
                start = line.index(":") + 1
                wifi_info["profile"] = line[start:].strip()
                break

        return wifi_info

    def connect_wifi_windows(self, network, profile):
        """ Connect to Wi-Fi on Windows

        :param network: network to connect to
        :param profile: network profile
        """
        if not profile:
            return
        try:
            subprocess.check_output(["netsh", "wlan", "connect", "ssid=" + network, "name=" + profile])
        except Exception as e:
            logging.error(str(e))

    def connect_wifi_linux(self, ssid, password):
        """ Connect Linux Wi-Fi

        :param ssid: connection SSID
        :param password: connection password
        """
        if not ssid and not password:
            logging.debug("Incomplete info")
            return

        psk = self.encrypt_psk(ssid, password)

        if psk and ssid:
            c = f"sudo nmcli con add con-name {ssid} type wifi ssid {ssid} wifi-sec.key-mgmt wpa-psk wifi-sec.psk {psk}"
            o = self.run_nmcli_command(c)
            logging.debug(f"{o}")

    def disconnect_wifi(self):
        """ Disconnect from Wi-Fi network """

        if "win" in sys.platform:
            self.disconnect_wifi_windows()
        else:
            self.disconnect_wifi_linux()

    def run_nmcli_command(self, command):
        """ Run nmcli command
        
        :param command: command string

        :return: command output
        """
        output = ""
        try:
            o = subprocess.check_output(command.split())
            output = o.decode("utf8")
        except Exception as e:
            logging.log(str(e))

        return output

    def get_ssid(self):
        """ Get SSID on Linux

        :return: SSID
        """
        c = "nmcli -f NAME,DEVICE -t c"
        o = self.run_nmcli_command(c)
        if o:
            lines = o.split()
            for line in lines:
                if "wlan" in line and line.find(":") != -1:
                    return line[0:line.find(":")]
        return None

    def disconnect_wifi_windows(self):
        """ Disconnect from Wi-Fi on Windows """

        try:
            subprocess.check_output(["netsh", "wlan", "disconnect", "interface=\"Wi-Fi\""])
        except Exception as e:
            logging.log(str(e))

    def disconnect_wifi_linux(self):
        """ Disconnect from Wi-Fi on Linux """

        ssid = self.get_ssid()
        if ssid == None:
            logging.log("Cannot disconnect wifi as SSID is not available")
            return

        logging.debug(f"Disconnecting SSID: {ssid}")
        c = f"sudo nmcli c delete {ssid}"
        o = self.run_nmcli_command(c)
        logging.debug(f"{o}")

    def get_linux_networks(self):
        """ Collect networks info on Linux

        :return: network info
        """
        wifi_info = {}
        networks = []
        names = []
        try:
            logging.debug("Collecting network info...")
            n = subprocess.check_output(["sudo", "nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"])
            lines = n.decode("utf8").split("\n")
            for line in lines:
                if line.startswith(":") or ":" not in line:
                    continue
                name, strength = line.split(":")
                if name in names:
                    continue
                networks.append({"name": name, "strength": int(strength)})
                names.append(name)
        except Exception as e:
            logging.error(e)

        wifi_info["profile"] = self.get_ssid()
        wifi_info["networks"] = networks

        return wifi_info

    def encrypt_psk(self, ssid, passphrase):
        """ Encrypt password

        :param ssid: SSID
        :param passphrase: password
        :return: encrypted password
        """
        psk = ""
        lines = []
        try:
            n = subprocess.check_output(["wpa_passphrase", ssid, passphrase])
            lines = n.decode("utf8").split("\n")
        except Exception as e:
            logging.error(str(e))

        if len(lines) == 0:
            return ""

        for line in lines:
            if "#psk=" in line:
                continue
            elif "psk=" in line:
                start = line.index("psk=") + len("psk=")
                psk += line[start:]

        return psk
