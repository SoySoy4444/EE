# Created 28 March 2021
from math import radians, tan, cos, sin, pi, sqrt, log

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def lambert_conformal_proj(lat, lon):
    lat0, lon0 = 39, -96 # reference latitude/longitude in cartopy default to (39, -96)
    s1, s2 = 33, 45 # standard parallels in cartopy default to (33, 45)
    R = 6371000

    lat, lon, lat0, lon0, s1, s2 = map(radians, [lat, lon, lat0, lon0, s1, s2])

    num = log(cos(s1)*(1/cos(s2))) # no secant function available
    denom = log(tan(pi/4+s2/2)*(1/tan(pi/4+s1/2))) # no cotangent function
    n = num / denom

    F = cos(s1)*(tan(pi/4+s1/2))**n/n
    p = R*F*((1/tan(pi/4+lat/2))**n)
    p0 = R*F*((1/tan(pi/4+lat0/2))**n)

    x = p*sin(n*(lon-lon0))
    y = p0-p*cos(n*(lon-lon0))

    print(lat, lon, lat0, lon0, s1, s2)
    print("num", num)
    print("denom", denom)
    print("n", n)
    print("F", F)
    print("p", p)
    print("p0", p0)
    print("x", x)
    print("y", y)
    print()
    return x, y


if __name__ == "__main__":
    nylat, nylon = 40.7128, -74.006
    madlat, madlon = 40.4168, -2.99
    toklat, toklon = 35.652832, 139.839478

    mer_nylat, mer_nylon = lambert_conformal_proj(nylat, nylon)
    mer_madlat, mer_madlon = lambert_conformal_proj(madlat, madlon)
    mer_toklat, mer_toklon = lambert_conformal_proj(toklat, toklon)

    print("City 1 calculation", mer_nylat, mer_nylon)
    print("City 2 calculation", mer_madlat, mer_madlon)
    print("City 3 calculation", mer_toklat, mer_toklon)

    distance = sqrt((mer_nylon-mer_madlon)**2+(mer_nylat-mer_madlat)**2)
    print("Distance Mad-NY", distance/1000)

    distance = sqrt((mer_toklon-mer_madlon)**2+(mer_toklat-mer_madlat)**2)
    print("Distance Mad-TOK", distance/1000)



    geodetic = ccrs.Geodetic()

    mer = ccrs.LambertConformal()
    nylon, nylat = mer.transform_point(nylon, nylat, geodetic)
    madlon, madlat = mer.transform_point(madlon, madlat, geodetic)
    toklon, toklat = mer.transform_point(toklon, toklat, geodetic)

    distance = sqrt((nylon-madlon)**2+(nylat-madlat)**2)
    print("Distance Mad-NY", distance/1000)

    distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
    print("Distance TOK-Mad", distance2/1000)
    #distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
   # print("Distance TOK-Mad", distance2)