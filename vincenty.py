from math import sqrt, atan, cos, sin, tan, radians, atan2

def vincenty(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # WGS-84 constants
    a = 6378137.0
    f = 1/298.257223563
    b = (1-f)*a
    
    u1 = atan((1-f)*tan(lat1))
    u2 = atan((1-f)*tan(lat2))
    L=lon2-lon1

    def iterate(old_lambda, previous_lambda):
        num_sig_figs = 12 #desired level of accuracy of lambda for recursion to end

        # print(old_lambda, previous_lambda)
        if "{0}".format(round(old_lambda, ndigits=num_sig_figs)) == "{0}".format(round(previous_lambda, ndigits=num_sig_figs)):
            return old_lambda
        else:
            # set variables as function attributes since they will be required outside of function scope
            iterate.sin_sigma = sqrt((cos(u2)*sin(old_lambda))**2+(cos(u1)*sin(u2)-sin(u1)*cos(u2)*cos(old_lambda))**2)
            iterate.cos_sigma = sin(u1)*sin(u2)+cos(u1)*cos(u2)*cos(old_lambda)
            iterate.sigma = atan2(iterate.sin_sigma, iterate.cos_sigma)

            sin_alpha = (cos(u1)*cos(u2)*sin(old_lambda))/iterate.sin_sigma
            iterate.cos_alpha_squared = 1-(sin_alpha)**2 #Pythagorean trig identity

            iterate.cos_2sigma_m = iterate.cos_sigma-(2*sin(u1)*sin(u2))/iterate.cos_alpha_squared

            C = f/16*iterate.cos_alpha_squared*(4+f*(4-3*iterate.cos_alpha_squared))

            new_lambda = L + (1-C)*f*sin_alpha*(iterate.sigma+C*iterate.sin_sigma*(iterate.cos_2sigma_m+C*iterate.cos_sigma*(-1+2*(iterate.cos_2sigma_m)**2)))
            return iterate(new_lambda, old_lambda)


    lambda_ = iterate(L, 0) #lambda_initial = L, no previous lambda
    
    u_squared = iterate.cos_alpha_squared*((a**2-b**2)/b**2)
    A = 1 + u_squared/16384*(4096+u_squared*(-768+u_squared*(320-175*u_squared)))
    B = u_squared/1024*(256+u_squared*(-128+u_squared*(74-47*u_squared)))

    delta_sigma = B*iterate.sin_sigma*(iterate.cos_2sigma_m+1/4*B*(iterate.cos_sigma*(-1+2*iterate.cos_2sigma_m)-B/6*iterate.cos_2sigma_m*(-3+4*(iterate.sin_sigma)**2)*(-3+4*(iterate.cos_2sigma_m)**2)))

    s = b * A *(iterate.sigma - delta_sigma)
    return s/1000 #/1000 for km, just s for metres

if __name__ == "__main__":
    city1 = (40.7128, -74.006) #New York
    city2 = (35.652832, 139.839478) #Tokyo
    city3 = (40.4168, -2.99) #Madrid

    distance = vincenty(*city1, *city2)
    print("Distance from New York to Tokyo:", distance)

    distance = vincenty(*city1, *city3)
    print("Distance from New York to Madrid:", distance)

    distance = vincenty(*city3, *city2)
    print("Distance from Madrid to Tokyo:", distance)

