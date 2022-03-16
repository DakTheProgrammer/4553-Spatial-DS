from ctypes.wintypes import POINT
import math
import json
import geopandas
import numpy
from shapely.geometry import Polygon

class Geo:
    #constructor that opens files needed and sets private variables for them
    def __init__(self):
        with open('continents.json') as f:
            self.__world = json.load(f)

        self.__output = open('Out.geojson', 'w')

    #returns the polygon of a given nation
    def getPoly(self, country):
        nation = self.__countryDic(country)

        multi = nation['geometry']['coordinates']

        poly = self.__makeSinglePoly(multi)

        return poly

    #finds the distance between 2 nations with a reduction formula using a box to reduce bordering points
    def getDistance(self, poly1, poly2, algo):
        if algo == True:
            center2 = self.getCenterPoint(poly1)
            center1 = self.getCenterPoint(poly2)

            tempRec = [center1, [center1[0], center2[1]], center2, [center2[0], center1[1]]]
            rec = Polygon(tempRec)

            con1 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly1], [y[1] for y in poly1]))
            con2 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly2], [y[1] for y in poly2]))
            
            #queries the borders with the rectangle
            pi1 = con1.sindex.query(rec)
            pi2 = con2.sindex.query(rec)

            distance = []

            #finds distance between 2 points
            for p1 in pi1:
                for p2 in pi2:
                    distance.append(math.sqrt(((con1[p1].x - con2[p2].x)**2)+((con1[p1].y-con2[p2].y)**2))) 

            ##########                output                      ####################
            ##########################################################################
            tempRec.append(tempRec[0])

            ps = []

            for points in pi1:
                ps.append([con1[points].x, con1[points].y])

            for points in pi2:
                ps.append([con2[points].x, con2[points].y])

            self.__geoJsonPoly(polys=[poly1, poly2, tempRec], points=ps)
            ##########################################################################
        else:
            con1 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly1], [y[1] for y in poly1]))
            con2 = geopandas.GeoSeries(geopandas.points_from_xy([x[0] for x in poly2], [y[1] for y in poly2]))

            distance = []

            for p1 in con1:
                for p2 in con2:
                    distance.append(math.sqrt(((p1.x - p2.x)**2)+((p1.y-p2.y)**2)))

        #finds shortest path
        distance.sort()

        return distance[0]

            


    #takes in a weight that reduces the polygon
    def reducePoints(self, name, weight):
        poly = self.getPoly(name)

        series = geopandas.GeoSeries(Polygon(poly))

        poly = series.simplify(weight)[0]
        poly = numpy.asarray(poly.exterior.coords).tolist()

        return poly

    #finds the center of a polygon
    def getCenterPoint(self, poly):
        temp = poly
        series = geopandas.GeoSeries(Polygon(poly))

        center = [series.centroid[0].x, series.centroid[0].y]

        return center

    def getCountries(self):
        out = []

        for continents in self.__world:
            for countries in self.__world[continents]:
                out.append(countries['properties']['name'])

        return out

    def getContinent(self, name):
        for continents in self.__world:
            for countries in self.__world[continents]:
                if name == countries['properties']['name']:
                    return continents


    #used to output data
    def __geoJsonPoly(self, polys = None, points = None):
        out = {
                "type": "FeatureCollection",
                "features": [
                    
                ]
            }

        if polys != None:
            for poly in polys:
                out['features'].append({
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            poly
                        ]
                    }
                })

        if points != None:
            for point in points:
                out['features'].append({
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Point",
                        "coordinates": point 
                    }
                })

        self.__output.write(json.dumps(out, indent=4))

    #takes a multi poly and breaks it down to a single one by finding the biggest
    def __makeSinglePoly(self, multi):
        i = 0
        max = 0
        index = 0
        
        for poly in multi:
            if len(poly[0]) > max:
                max = len(poly[0])
                index = i
            i += 1

        return multi[index][0]

    #finds the desired country
    def __countryDic(self, country):
        for continents in self.__world:
            for countries in self.__world[continents]:
                if countries['properties']['name'].lower() == country.lower():
                    return countries
        
#testing
if __name__ == "__main__":
    g = Geo()

    p1 = g.reducePoints('Iran', .1)
    p2 = g.reducePoints('Aruba', .1)

    print(g.getDistance(p1, p2, False))