# Created 27 March 2021

from math import radians, log, tan, pi, sqrt

import cartopy.crs as ccrs

def mercator_proj(lat, lon):
    lat, lon = map(radians, [lat, lon])

    R = 6371000
    lon_0 = 0
    x = R*(lon-lon_0)
    y = R*log(tan(pi/4+lat/2))
    return x, y


if __name__ == "__main__":
    nylat, nylon = 40.7128, -74.006
    madlat, madlon = 40.4168, -2.99
    toklat, toklon = 35.652832, 139.839478

    mer_nylat, mer_nylon = mercator_proj(nylat, nylon)
    mer_madlat, mer_madlon = mercator_proj(madlat, madlon)
    mer_toklat, mer_toklon = mercator_proj(toklat, toklon)

    print("City 1 calculation", mer_nylat, mer_nylon)
    print("City 2 calculation", mer_madlat, mer_madlon)
    print("City 3 calculation", mer_toklat, mer_toklon)

    distance = sqrt((mer_nylon-mer_madlon)**2+(mer_nylat-mer_madlat)**2)
    print("Distance Mad-NY", distance)

    distance = sqrt((mer_toklon-mer_madlon)**2+(mer_toklat-mer_madlat)**2)
    print("Distance Mad-TOK", distance)



    geodetic = ccrs.Geodetic()

    mer = ccrs.Mercator()
    nylon, nylat = mer.transform_point(nylon, nylat, geodetic)
    madlon, madlat = mer.transform_point(madlon, madlat, geodetic)
    toklon, toklat = mer.transform_point(toklon, toklat, geodetic)

    distance = sqrt((nylon-madlon)**2+(nylat-madlat)**2)
    print("Distance Mad-NY", distance)

    distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
    print("Distance TOK-Mad", distance2)
    #distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
   # print("Distance TOK-Mad", distance2)