"""
X Plane STAR Practice Tool Python plugin
Copyright (C) 2018 Rafael Garcia Argente
https://github.com/rgargente/XPlaneStarPracticeTool

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
This is the code that deals directly with the X-Plane SDK. It is not easily testable and thus it is isolated.
It is created as a class instead of a simple collection of functions so that we can use a mock object for testing purposes.
"""
from XPLMNavigation import *
from XPLMDataAccess import *


# xplm_Nav_Unknown: "UKN",
# xplm_Nav_Airport: "APT",
# xplm_Nav_NDB: "NDB",
# xplm_Nav_VOR: "VOR",
# xplm_Nav_ILS: "ILS",
# xplm_Nav_Localizer: "LOC",
# xplm_Nav_GlideSlope: "GS",
# xplm_Nav_OuterMarker: "OM",
# xplm_Nav_MiddleMarker: "MM",
# xplm_Nav_InnerMarker: "IM",
# xplm_Nav_Fix: "FIX",
# xplm_Nav_DME: "DME",
# xplm_Nav_LatLon: "L/L"}

class XplmWrapper:

    def get_airport_lat_lon(self, id, airport_lat, airport_lon):
        ref = XPLMFindNavAid(None, id, airport_lat, airport_lon,
                             None, xplm_Nav_Airport)
        if ref == XPLM_NAV_NOT_FOUND:
            return None, None

        out_lat, out_long, out_id = [], [], []
        XPLMGetNavAidInfo(ref, None, out_lat, out_long, None, None, None, out_id, None, None)
        if out_id[0] == id:
            return out_lat[0], out_long[0]
        else:
            return None, None

    #TODO Shouldnt be needed
    def get_waypoint_lat_lon(self, id, airport_lat, airport_lon):
        ref = XPLMFindNavAid(None, id, airport_lat, airport_lon,
                             None, xplm_Nav_Airport | xplm_Nav_NDB | xplm_Nav_VOR | xplm_Nav_Fix)
        if ref == XPLM_NAV_NOT_FOUND:
            return None, None
        else:
            out_lat, out_long = [], []
            XPLMGetNavAidInfo(ref, None, out_lat, out_long, None, None, None, None, None, None)
            return out_lat[0], out_long[0]

    def get_aircraft_lat_lon(self):
        lat_dr = XPLMFindDataRef("sim/flightmodel/position/latitude")
        lon_dr = XPLMFindDataRef("sim/flightmodel/position/longitude")
        return XPLMGetDataf(lat_dr), XPLMGetDataf(lon_dr)

    def get_nearest_airport(self):
        lat, lon = self.get_aircraft_lat_lon()
        ref = XPLMFindNavAid(None, None, lat, lon, None, xplm_Nav_Airport)
        if ref == XPLM_NAV_NOT_FOUND:
            return None, None
        else:
            out_lat, out_lon, out_id, out_name = [], [], [], []
            XPLMGetNavAidInfo(ref, None, out_lat, out_lon, None, None, None, out_id, out_name, None)
            return out_id[0], out_name[0], out_lat[0], out_lon[0]
