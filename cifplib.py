import os


def _get_file_path(xplane_path, airport_icao):
    file_name = "{}.dat".format(airport_icao)
    file_path = os.path.join(xplane_path, "Custom Data", "CIFP", file_name)
    if not os.path.exists(file_path):
        file_path = os.path.join(xplane_path, "Resources", "default data", "CIFP", file_name)
    return file_path


class Cifp:

    def __init__(self, xplane_path=None, airport_icao=None, file_path=None):
        """
        Either (xplane_path and airport_icao) or file_path should be passed.
        :param file_path: If None xplane_path and airport_icao are used to find the right path. Otherwise they are ignored and the passed path is used.
        """
        self.raw_lines = []
        self.star_names = set()
        self.stars = {}

        if not file_path:
            file_path = _get_file_path(xplane_path, airport_icao)

        f = open(file_path)
        for l in f:
            self.raw_lines.append(l)
            # STAR:010, 2, MAPA1K, RW30, MAPAX, LE, E, A, E,, , IF,, , , , , , , , , , , , , , , , , , , , , , , , , ;
            # STAR:020, 2, MAPA1K, RW30,, , , , , , , CI,, , , , , , , , 1690,, , , , , , , , , , , , , , , , ;
            if l.split(':')[0] == 'STAR':
                line_items = l.split(',')
                star_name = line_items[2]
                if star_name not in self.star_names:  # new STAR
                    self.star_names.add(star_name)
                    star = Star(star_name)
                    self.stars[star_name] = star
                else:  # update star
                    star = self.stars[star_name]
                star._parse_raw_line(line_items)


class Star:
    INDEX_WAYPOINT = 4
    INDEX_COURSE_INTERCEPT = 11
    INDEX_CI_HEADING = 20

    def __init__(self, name):
        self.name = name
        self.waypoints = []
        self.init_lat = 0.0
        self.init_lon = 0.0
        self.init_heading = None

    def _parse_raw_line(self, line_items):
        if line_items[self.INDEX_COURSE_INTERCEPT] == 'CI':
            self.init_heading = float(line_items[self.INDEX_CI_HEADING]) / 10
            self.waypoints.append('INTC')
        else:
            self.waypoints.append(line_items[self.INDEX_WAYPOINT])
