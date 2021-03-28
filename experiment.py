import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from math import *
from projections.mollweide import mollweide_proj
from projections.mercator import mercator_proj
from haversine import haversine_formula

nylat, nylon = 40.7128, -74.006
madlat, madlon = 40.4168, -2.99
toklat, toklon = 35.652832, 139.839478

print("City 1 calculation", mollweide_proj(nylat, nylon))
print("City 2 calculation", mollweide_proj(madlat, madlon))
print("City 3 calculation", mollweide_proj(toklat, toklon))



proj = ccrs.Mollweide(central_longitude=0, globe=None)
#proj._threshold /= 10.
ax = plt.axes(projection=proj)

ax.set_global()
ax.stock_img()

ax.coastlines()
#ax.set_extent((-120, 120, -180, 180))
#ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='face', facecolor='b'))

#[x_1, x_2] (E/W), [y_1, y_2] (N/S)
#plt.plot([-0.08, 132], [51.53, 43.17], color='red',  transform=ccrs.Geodetic())
#plt.plot([-0.08, 132], [51.53, 43.17], color='blue', transform=ccrs.PlateCarree())


#New york and Madrid
#plt.plot([-74.006, -3.7038], [40.7128, 40.4168], color='red',  transform=ccrs.Geodetic())
#plt.plot([-74.006, -3.7038], [40.7128, 40.4168], color='blue', transform=ccrs.PlateCarree())


#ax.set_xlim(-180, 180)


"""
geodetic = ccrs.Geodetic()

moll = ccrs.Mollweide()
nylon, nylat = moll.transform_point(nylon, nylat, geodetic)
madlon, madlat = moll.transform_point(madlon, madlat, geodetic)
toklon, toklat = moll.transform_point(toklon, toklat, geodetic)

print("City 1 simulation", nylat, nylon)
print("City 2 simulation", madlat, madlon)
print("City 3 simulation", toklat, toklon)


distance = sqrt((nylon-madlon)**2+(nylat-madlat)**2)
print("Distance Mad-NY", distance)

distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
print("Distance TOK-Mad", distance2)

print("Ratio mad-ny/tok-mad", distance/distance2)

#New york and beijing #lon, then lat
#plt.plot([-74.006, 116.383331], [40.7128, 39.916668], color='red',  transform=ccrs.Geodetic())
#plt.plot([-74.006, 116.383331], [40.7128, 39.916668], color='blue', transform=ccrs.PlateCarree())
plt.plot([nylon, madlon], [nylat, madlat], color='green', transform=moll)
plt.plot([toklon, madlon], [toklat, madlat], color='red', transform=moll)

plt.show()
"""


geodetic = ccrs.Geodetic()

mer = ccrs.Gnomonic(central_latitude=76.0972, central_longitude=68.0326)
nylon, nylat = mer.transform_point(nylon, nylat, geodetic)
madlon, madlat = mer.transform_point(madlon, madlat, geodetic)
toklon, toklat = mer.transform_point(toklon, toklat, geodetic)

print(nylat, nylon)
print(madlat, madlon)
print(toklat, toklon)
distance = sqrt((nylon-madlon)**2+(nylat-madlat)**2)
print("Distance Mad-NY", distance/1000)

distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
print("Distance TOK-Mad", distance2/1000)

print("Ratio mad-ny/tok-mad", distance/distance2)