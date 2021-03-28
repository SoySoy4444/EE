# Created 28 March 2021
# http://www.notespoint.com/aitken-interpolation/
# https://www.python-course.eu/polynomial_class_in_python.php

from math import sqrt, radians
import cartopy.crs as ccrs
from itertools import zip_longest

class Polynomial:
    def __init__(self, *coefficients):
        self.coefficients = list(coefficients)
     
    def __repr__(self):
        # canonical string representation
        return f"Poly {tuple(self.coefficients)}"

    def __str__(self):
        #return mathjax style
        string = ""
        for count, term in enumerate(self.coefficients):
            degree = len(self.coefficients) - count - 1

            if term > 0:
                term = "+" + str(term)
            if str(term) == "+1" and degree!=0: #need +1 for a constant, i.e. degree 0
                term = "+"
            elif str(term) == "-1" and degree!=0:
                term = "-"
            elif term == 0: #terms with a 0 coefficient do not need to be printed e.g. 0x^2
                continue
            string += f"{term}x^{degree}"

        if string[0] == "+": # first term, if positive, does not need + sign e.g. +x^3-2x -> x^3-2x
            string = string[1:]
        string = string.replace("x^0", "") # constants do not need x^0 attached eg 4x+3x^0 -> 4x+3
        string = string.replace("x^1","x") # x^1 -> just x

        return string

    def __call__(self, x):    
        res = 0
        for degree, coefficient in enumerate(self.coefficients[::-1]):
            res += coefficient * x**degree
        return res

    def __mul__(self, p): #self * p
        if isinstance(p, Polynomial): #if the multiplier is a polynomial, do polynomial multiplication 
            #length of coefficients of polynomial p gives (degree of p) + 1
            #therefore len(p)+len(q) = deg(p)+1 + def(q)+1 = deg(p)+deg(q)+2

            #resulting polynomial p*q has degree deg(p)+deg(q) e.g. cubic * quadratic = quintic
            #such a polynomial of degree deg(p)+deg(q) has deg(p)+deg(q)+1 terms e.g. quadratic has 3 terms, x^2, x^1, x^0
            #we want number of terms = deg(p)+deg(q)+1

            #therefore deg(p)+deg(q)+1=len(p)+len(q)-1

            res = [0]*(len(self.coefficients)+len(p.coefficients)-1) #create an array filled with 0s with as many terms as the resulting polynomial
            

            for self_degree, self_coefficient in enumerate(self.coefficients): #for each term in self
                for p_degree, p_coefficient in enumerate(p.coefficients): #for each term in p
                    #product of two terms p*q has degree deg(p)+deg(q) and coefficient p*q
                    res[self_degree+p_degree] += self_coefficient*p_coefficient

        elif isinstance(p, float) or isinstance(p, int): #scalar multiplication
            #multiply each coefficient by the scalar p
            res = [p*coefficient for coefficient in self.coefficients]
        else: #error, invalid operation
            print("TRIGG")
            print(type(p))
        return Polynomial(*res)

    __rmul__ = __mul__ #handle p*self

    def __add__(self, p):
        c1 = self.coefficients[::-1]
        c2 = p.coefficients[::-1]
        res = [sum(t) for t in zip_longest(c1, c2, fillvalue=0)]
        return Polynomial(*res[::-1])
    
    def __sub__(self, p):
        c1 = self.coefficients[::-1]
        c2 = p.coefficients[::-1]
        
        res = [t1-t2 for t1, t2 in zip_longest(c1, c2, fillvalue=0)]
        return Polynomial(*res[::-1])


# | a b |
# | c d |
def det(a, b, c, d) -> "Polynomial":
    return a*d-c*b

def aitkin(x:"list", y:"list", value:"float") -> "float":
    deltas = [y]

    for stage_num in range(1, len(x)):
        deltas.append([])
        for j in range(1, len(x)-stage_num+1):
            # print("stagenum", stage_num, "j", j)

            a = deltas[stage_num-1][0] if isinstance(deltas[stage_num-1][0], Polynomial) else Polynomial(deltas[stage_num-1][0])
            c = deltas[stage_num-1][j] if isinstance(deltas[stage_num-1][j], Polynomial) else Polynomial(deltas[stage_num-1][j])

            p = det(a, Polynomial(-1, x[stage_num-1]), c, Polynomial(-1, x[stage_num+j-1]))
            p *= 1/(x[stage_num+j-1]-x[stage_num-1])
            # print(p)
            # print(p(value))
            # print()
            deltas[stage_num].append(p)
        # print("-"*50)

    final_polynomial = deltas[-1][0]
    return final_polynomial(value)

def robinson(lat, lon):
    latitudes = [5*i for i in range(19)] #generate 0 degrees - 90 degrees
    X_values = [1, 0.9986, 0.9954, 0.99, 0.9822, 0.973, 0.96, 0.9427, 0.9216, 0.8962, 0.8679, 0.835, 0.7986, 0.7597, 0.7186, 0.6732, 0.6213, 0.5722, 0.5322]
    Y_values = [0, 0.062, 0.124, 0.186, 0.248, 0.31, 0.372, 0.434, 0.4958, 0.5571, 0.6176, 0.6769, 0.7346, 0.7903, 0.8435, 0.8936, 0.9394, 0.9761, 1]

    X = aitkin(latitudes, X_values, lat)
    Y = aitkin(latitudes, Y_values, lat)

    R = 6378137 #radius of the earth in metres
    lon0 = 0
    lon, lon0 = map(radians, [lon, lon0])
    x = 0.8487*R*X*(lon-lon0)
    y = 1.3523*R*Y
    return x, y


if __name__ == "__main__":
    nylat, nylon = robinson(40.7128, -74)
    toklat, toklon = robinson(35.6762, 139.6503)

    distance = sqrt((nylat-toklat)**2+(nylon-toklon)**2)
    print("Distance TOK-NY", distance/1000)

    nylat, nylon = (40.7128, -74)
    toklat, toklon = (35.6762, 139.6503)

    geodetic = ccrs.Geodetic()

    robin = ccrs.Robinson()
    nylon, nylat = robin.transform_point(nylon, nylat, geodetic)
    toklon, toklat = robin.transform_point(toklon, toklat, geodetic)
    print(toklat, toklon)
    distance = sqrt((nylon-toklon)**2+(nylat-toklat)**2)
    print("Distance Tok-NY", distance/1000)
