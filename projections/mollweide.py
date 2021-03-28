# Created 27 March 2021
from math import sin, cos, radians, pi, sqrt

def mollweide_proj(lat, lon):
    count = 0

    #Recursive function for Newton-Raphson method to calculate theta
    def newton(old_theta, lat, count):
        # print(f"Iteration {count}, current value {old_theta}")
        if count > 50:
            return old_theta
        else:
            new_theta = old_theta-(2*old_theta+sin(2*old_theta)-pi*sin(radians(lat)))/(2+2*cos(2*old_theta))
            count += 1
            return newton(new_theta, lat, count)
    R = 6371000 #radius of Earth in m (unit used by cartopy for mollweide, min 1.804*10^7 = R*2sqrt(2))
    c = 0 #central meridian, Greenwich

    theta = newton(radians(lat), lat, count)
    print(theta)

    x = R*2*sqrt(2)/pi*(radians(lon)-c)*cos(theta)
    y = R*sqrt(2)*sin(theta)
    return (x, y)

if __name__ == "__main__":
    nylat, nylon = 40.7128, -74.006
    madlat, madlon = 40.4168, -2.99
    toklat, toklon = 35.652832, 139.839478

    moll_nylat, moll_nylon = mollweide_proj(nylat, nylon)
    moll_madlat, moll_madlon = mollweide_proj(madlat, madlon)

    print("City 1 calculation", moll_nylat, moll_nylon)
    print("City 2 calculation", moll_madlat, moll_madlon)
    print("City 3 calculation", mollweide_proj(toklat, toklon))

    distance = sqrt((moll_nylon-moll_madlon)**2+(moll_nylat-moll_madlat)**2)
    print("Distance Mad-NY", distance)

    #distance2 = sqrt((toklon-madlon)**2+(toklat-madlat)**2)
   # print("Distance TOK-Mad", distance2)

