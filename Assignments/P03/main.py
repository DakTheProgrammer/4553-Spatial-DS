import json
import numpy 
import pandas
import geopandas
import shapely

import matplotlib.pyplot as plt
from shapely.ops import unary_union
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area

#opens necessary files
border = geopandas.read_file("us_border_shp/us_border.shp")
cities = geopandas.read_file("cities.geojson")
ufo = pandas.read_csv("BetterUFOData.csv")

#ufo geoframe
ufo = geopandas.GeoDataFrame(ufo, geometry=geopandas.points_from_xy(ufo.lon, ufo.lat))

#size of plots
fig, ax = subplot_for_map(figsize=(12, 10))

#creates the diagram
border_proj = cities.to_crs(border.crs)
border_shape = unary_union(border.geometry)
coords = points_to_coords(border_proj.geometry)
region_polys, region_pts = voronoi_regions_from_coords(coords, border_shape)

#Plots voronoi to be shown
plot_voronoi_polys_with_points_in_area(ax, border_shape, region_polys, coords, region_pts)

#plt.show() #<----------------uncomment to see map

#used to append dictionary
temp = len(region_polys)
i = temp

for points in list(ufo.values):
    region_polys.update({temp : points[7]})
    temp += 1

#creates r tree with all points and polys in it
rtree = geopandas.GeoSeries(region_polys)

out = []

for poly in range(0, i):
    #makes sure the right poly is used so output is accurate
    if(type(rtree[poly]) == shapely.geometry.polygon.Polygon):
        ty = 'Single'
        polypoints = numpy.asarray(rtree[poly].exterior.coords)
        polypoints = polypoints.tolist()
    else:
        ty = 'Multi'
        polypoints = []
        for polygon in rtree[poly]:
            coords = numpy.asarray(polygon.exterior.coords)
            coords = coords.tolist()
            polypoints.append(coords)

    #runs query to get all ufos in poly
    que = rtree.sindex.query(rtree[poly])

    ps = []

    for points in que:
        #makes sure to only return points and not border polys
        if type(rtree[points]) == shapely.geometry.point.Point:
            ps.append([rtree[points].x, rtree[points].y])

    out.append({
        'type': ty,
        'poly': polypoints,
        'points': ps
    })

with open('PointsInPolys.json', 'w') as f:
    f.write(json.dumps(out))  