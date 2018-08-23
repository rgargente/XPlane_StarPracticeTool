import os


def get_airport_file_path(xplane_path, airport_icao):
    file_name = "{}.dat".format(airport_icao)
    file_path = os.path.join(xplane_path, "Custom Data", "CIFP", file_name)
    if not os.path.exists(file_path):
        file_path = os.path.join(xplane_path, "Resources", "default data", "CIFP", file_name)
    return file_path
