import re

from starpracticetool_lib.mathlib import is_number


class FixParser:
    def __init__(self, fix_filepath):
        self.fixes = {}

        with open(fix_filepath) as f:
            for l in f:
                l = re.sub(' +', ' ', l.strip())  # Remove multiple spaces
                parts = l.split(' ', 5)
                if len(parts) == 5 \
                        and is_number(parts[0]) and is_number(parts[1]):
                    self.fixes[parts[2]] = (float(parts[0]), float(parts[1]))


    def get_coord(self, fixname):
        return self.fixes[fixname]