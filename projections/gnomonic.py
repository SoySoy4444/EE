# Created 28 March, 2021
from math import sqrt, radians, sin, cos
import cartopy.crs as ccrs


def gnomonic_proj(lat, lon):
    lat0, lon0 = 0, 0
    lat, lon, lat0, lon0 = map(radians, [lat, lon, lat0, lon0])

    print(lat, lon, lat0, lon0)

    cosC = (sin(lat)*sin(lat0))+(cos(lat)*cos(lat0)*cos(lon-lon0)) #angular distance of x, y from centre of projection
    x = (cos(lat)*sin(lon-lon0))/cosC
    y = (cos(lat0)*sin(lat)-sin(lat0)*cos(lat)*cos(lon-lon0))/cosC

    print(cosC)
    print(x, y)
    print()
    return x, y


if __name__ == "__main__":
    nylat, nylon = 40.7128, -74.006
    madlat, madlon = 40.4168, -2.99
    toklat, toklon = 35.652832, 139.839478

    mer_nylat, mer_nylon = gnomonic_proj(nylat, nylon)
    mer_madlat, mer_madlon = gnomonic_proj(madlat, madlon)
    mer_toklat, mer_toklon = gnomonic_proj(toklat, toklon)

    print("City 1 calculation", mer_nylat, mer_nylon)
    print("City 2 calculation", mer_madlat, mer_madlon)
    print("City 3 calculation", mer_toklat, mer_toklon)

    distance = sqrt((mer_nylon-mer_madlon)**2+(mer_nylat-mer_madlat)**2)
    print("Distance Mad-NY", distance/1000*6371000)

    distance = sqrt((mer_toklon-mer_madlon)**2+(mer_toklat-mer_madlat)**2)
    print("Distance Mad-TOK", distance/1000*6371000)



    geodetic = ccrs.Geodetic()

    mer = ccrs.Gnomonic()
    nylon, nylat = mer.transform_point(nylon, nylat, geodetic)
    madlon, madlat = mer.transform_point(madlon, madlat, geodetic)
    toklon, toklat = mer.transform_point(toklon, toklat, geodetic)

    distance = sqrt((nylon-madlon)**2+(nylat-madlat)**2)
    print("Distance Mad-NY", distance/1000)

    distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
    print("Distance TOK-Mad", distance2/1000)
    #distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
   # print("Distance TOK-Mad", distance2)