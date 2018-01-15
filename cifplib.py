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

        if not file_path:
            file_path = _get_file_path(xplane_path, airport_icao)

        f = open(file_path)
        for l in f:
            self.raw_lines.append(l)
            """
            STAR:010,2,CEGA1K,RW30,CEGAM,LE,E,A,E C , ,   ,IF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
            STAR:020,2,CEGA1K,RW30,LEKTO,LE,P,C,E   , ,   ,TF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
            """
            if l.split(':')[0] == 'STAR':
                self.star_names.add(l.split(',')[2])
