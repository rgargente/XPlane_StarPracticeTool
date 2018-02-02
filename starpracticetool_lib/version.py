VERSION = "0.9.0"

import urllib2

version_url= "https://raw.githubusercontent.com/rgargente/XPlane_StarPracticeTool/master/starpracticetool_lib/version.txt"
response = urllib2.urlopen(version_url, timeout=0.5).read()
print(response)