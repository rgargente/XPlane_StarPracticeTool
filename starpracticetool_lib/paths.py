import os


def get_default_data_path(xplane_path):
    return os.path.join(xplane_path, "Resources", "default data")


def get_custom_data_path(xplane_path):
    return os.path.join(xplane_path, "Custom Data")


def _get_file_path(xplane_path, file_name):
    file_path = os.path.join(get_custom_data_path(xplane_path), file_name)
    if not os.path.exists(file_path):
        file_path = os.path.join(get_default_data_path(xplane_path), file_name)
    return file_path


def get_airport_file_path(xplane_path, airport_icao):
    file_name = os.path.join("CIFP", "{}.dat".format(airport_icao))
    return _get_file_path(xplane_path, file_name)


def get_earth_fix_dat_file_path(xplane_path):
    return _get_file_path(xplane_path, "earth_fix.dat")


def get_earth_nav_dat_file_path(xplane_path):
    return _get_file_path(xplane_path, "earth_nav.dat")
