from starpracticetool_lib.mathlib import is_number


class FixParser:
    def __init__(self, filepath):
        self.fixes = []
        with open(filepath) as f:
            for l in f:
                parts = l.split(' ', 5)
                if len(parts) == 5 \
                        and is_number(parts[0]) and is_number(parts[1]):
                    self.fixes.append((float(parts[0]), float(parts[1]), parts[2]))