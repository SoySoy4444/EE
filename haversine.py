# Created 27 March 2021

from math import radians, sin, cos, asin, sqrt

def haversine_formula(lat1, lon1, lat2, lon2):
    R = 6371000 # radius of Earth in metres
    # convert latitudes and longitudes to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    inside = sin((lat2-lat1)/2)**2+cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
    d = 2*R*asin(sqrt(inside))
    return d

if __name__ == "__main__":
    nylat, nylon = 40.7128, -74.006
    madlat, madlon = 40.4168, -2.99
    toklat, toklon = 35.652832, 139.839478

    print("NY - Madrid", haversine_formula(nylat, nylon, madlat, madlon)/1000)
    print("Madrid - Tokyo", haversine_formula(madlat, madlon, toklat, toklon)/1000)
    print("NY - Tokyo", haversine_formula(nylat, nylon, toklat, toklon)/1000)