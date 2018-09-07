"""
This script creates a release package for the plugin and updates the version.txt file
"""

import glob
import os
import zipfile

from starpracticetool_lib.version import VERSION

if __name__ == '__main__':
    zipf = zipfile.ZipFile('PI_StarPracticeTool_v{}.zip'.format(VERSION), 'w', zipfile.ZIP_DEFLATED)
    zipf.write('PI_StarPracticeTool.py')
    zipf.write('StarPracticeTool_License.txt')
    for f in glob.glob('starpracticetool_lib/*.py'):
        zipf.write(f)
    zipf.close()

    with open(os.path.join('starpracticetool_lib', 'version.txt'), 'w') as verf:
        verf.write(VERSION)
