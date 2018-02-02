"""
This script creates a release package for the plugin
"""

import os
import zipfile

from starpracticetool_lib.version import VERSION

if __name__ == '__main__':
    zipf = zipfile.ZipFile('PI_StarPracticeTool_v{}.zip'.format(VERSION), 'w', zipfile.ZIP_DEFLATED)
    zipf.write('PI_StarPracticeTool.py')
    zipf.write('StarPracticeTool_License.txt')
    zipf.write(os.path.join('starpracticetool_lib', '__init__.py'))
    zipf.write(os.path.join('starpracticetool_lib', 'cifplib.py'))
    zipf.write(os.path.join('starpracticetool_lib', 'mathlib.py'))
    zipf.write(os.path.join('starpracticetool_lib', 'version.py'))
    zipf.write(os.path.join('starpracticetool_lib', 'xplm_wrapper.py'))
    zipf.close()