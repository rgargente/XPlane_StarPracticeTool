"""
This is the code that deals directly with the X-Plane SDK. It is not easily testable and thus it is isolated.
It is created as a class instead of a simple collection of functions so that we can use a mock object for testing purposes.
"""
from XPLMNavigation import *


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

    def get_waypoint_lat_lon(self, id, airport_lat, airport_lon):
        ref = XPLMFindNavAid(None, id, airport_lat, airport_lon,
                             None, [xplm_Nav_Airport, xplm_Nav_NDB, xplm_Nav_VOR, xplm_Nav_Fix])
        out_lat, out_long = [], []
        XPLMGetNavAidInfo(ref, None, out_lat, out_long, None, None, None, None, None, None)
        return out_lat[0], out_long[0]

    def get_aircraft_lat_long(self):
        lat_dr = XPLMFindDataRef("sim/flightmodel/position/latitude")
        lon_dr = XPLMFindDataRef("sim/flightmodel/position/longitude")
        return XPLMGetDataf(lat_dr), XPLMGetDataf(lon_dr)

    def get_nearest_airport(self):
        lat, lon = get_aircraft_lat_long()
        ref = XPLMFindNavAid(None, None, lat, lon, None, xplm_Nav_Airport)
        if ref == XPLM_NAV_NOT_FOUND:
            return None, None
        else:
            out_lat, out_lon, out_id, out_name = [], [], [], [], []
            XPLMGetNavAidInfo(ref, None, out_lat, out_lon, None, None, None, out_id, out_name, None)
            return out_id[0], out_name[0], out_lat[0], out_lon[0]
