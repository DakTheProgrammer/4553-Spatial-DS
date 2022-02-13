import csv
import json
from statistics import mean
import geopandas
from numpy import sort
from shapely.geometry import Point


with open('cities.geojson') as f:
    cities = json.load(f)

ufo = []

with open('ufo_data.csv') as f:
    csvfile = csv.DictReader(f, delimiter = ',')

    for row in csvfile:
        #loads csv dictionary into an array
        ufo.append(row)

points = []
names = []
#makes the outline for points as well as keys for city names
for feature in cities["features"]:
    if feature["geometry"]["type"] == "Point":
        points.append(feature["geometry"]["coordinates"])
        names.append(feature['properties']['city'])

cities = []
for point in points:
    cities.append(Point(point))

#makes geo series of all cities
geo = geopandas.GeoSeries(cities)

output = []

for i in range(len(geo)):
    dist = []

    arr = geo.distance(geo[i])

    #converts result to an array
    arr = arr.values 

    for i in range(len(arr)):
        if arr[i] != 0:
            #makes tuple to store all distances
            dist.append((names[i], arr[i]))

    #sorts the nearest cities
    dist.sort(key= lambda x: x[1])

    city = {
        'city': names[i],
        'longitude': geo[i].x,
        'latitude': geo[i].y,
        'distance': dist
    }

    output.append(city)

#writes the distances of all cities to json file
with open('distances.json', 'w') as f:
    f.write(json.dumps(output))

#creates points of all ufos
points = []
for dics in ufo:
    points.append(Point(float(dics['lon']), float(dics['lat'])))

#geoseries of all ufos
geoufo = geopandas.GeoSeries(points)

output = []
for i in range(len(geo)):
    dist = []

    arr = geoufo.distance(geo[i])

    arr = arr.values

    #sorts the array based on closest ufo sightings
    arr = sort(arr)

    #gets only the top 100 nearest ufos
    top = arr[0:100]

    #finds the average of the 100 closest ufos
    avg = round(mean(top), 18)

    city = {
        'city': names[i],
        'longitude': geo[i].x,
        'latitude': geo[i].y,
        'avgufo': avg
    }

    output.append(city)

#writes average distance of closest ufos to file
with open('average_ufo.json', 'w') as f:
    f.write(json.dumps(output))    