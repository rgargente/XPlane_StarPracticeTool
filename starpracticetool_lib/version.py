VERSION = "1.1.0"

import socket
import urllib

socket.setdefaulttimeout(1) #second

version_url = "https://raw.githubusercontent.com/rgargente/XPlane_StarPracticeTool/master/starpracticetool_lib/version.txt"
last_version = None
try:
    last_version = urllib.urlopen(version_url)
    last_version = last_version.readline()
except:
    pass


def is_up_to_date():
    return VERSION == last_version