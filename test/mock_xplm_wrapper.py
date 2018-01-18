class MockXplmWrapper:

    def get_waypoint_lat_lon(self, id, airport_lat, airport_lon):
        if id == 'LEBB':
            return 43.304305556, -2.922277778
        elif id == 'DGO':
            return 42.453305556, -2.880694444
        elif id == 'VRA':
            return 42.731888889, -2.865583333
        elif id == 'MAPAX':
            return 43.683750000, -3.044083333
        else:
            return None, None
