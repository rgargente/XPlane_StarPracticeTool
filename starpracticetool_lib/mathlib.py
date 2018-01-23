import math


def heading_and_speed_to_xyz_vector(heading, speed_ms):
    """
    Converts a heading and speed to a velocity vector in XPlane's Open GL coordinates.
    Coordinate system is right handed, Y up. X is East
    :param heading: in degrees 
    :param speed_ms: in m/s
    :return: [x, y, z]
    """
    alpha = math.radians(heading - 90)
    x = math.cos(alpha) * speed_ms
    z = math.sin(alpha) * speed_ms
    return [x, 0, z]


def hpr_to_quaternion(heading, pitch, roll):
    heading = math.radians(heading)
    pitch = math.radians(pitch)
    roll = math.radians(roll)

    cos1 = math.cos(roll / 2)
    cos2 = math.cos(pitch / 2)
    cos3 = math.cos(heading / 2)
    sin1 = math.sin(roll / 2)
    sin2 = math.sin(pitch / 2)
    sin3 = math.sin(heading / 2)

    q = []
    q.append(cos1 * cos2 * cos3 + sin1 * sin2 * sin3)
    q.append(sin1 * cos2 * cos3 - cos1 * sin2 * sin3)
    q.append(cos1 * sin2 * cos3 + sin1 * cos2 * sin3)
    q.append(cos1 * cos2 * sin3 - sin1 * sin2 * cos3)
    return q


def knots_to_m_sec(kts):
    """Knots (kt) to meters/second (m/s)"""
    return kts * 0.514444
