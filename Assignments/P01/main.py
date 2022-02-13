import json

with open('cities_latlon_w_pop.json') as file:
    info = json.load(file)

#list of colors to use for markers
colors = ['#9987a0', '#34f81e', '#c65776', '#8a0115', '#916709', '#5bb162', '#1b4ee8', '#c38099',
'#8303af', '#eadafb', '#c59844', '#9993e6', '#645150', '#2e0bdf', '#34dc76', '#1d2898',
'#89de84', '#a68c5f', '#228e51', '#b7ed5b', '#9fcc82', '#fde317', '#261a3b', '#ddd262',
'#e20b69', '#2ff233', '#db3f86', '#555f92', '#71ac92', '#a0e2bb', '#883101', '#4dec44',
'#f18ad8', '#b56bbc', '#0982ba', '#8d92b3', '#909ee6', '#fc6afc', '#a0713d', '#966d37',
'#1aea6d', '#d448b3', '#af8218', '#87e18b', '#4a296c', '#004a00', '#286df9', '#1e4b45', '#4b527d'] 

states = {}

#Removes Hawaii and Alaska from the equation and loads highest population cities for each state
for dics in info:
    if dics['state'] != 'Alaska' and dics['state'] != 'Hawaii':
        if dics['state'] not in states or states[dics['state']]['population'] < dics['population']:
            states.update({
                dics['state'] : {
                "city": dics['city'],
                "growth": dics['growth'],
                "latitude": dics['latitude'],
                "longitude": dics['longitude'],
                "population": dics['population'],
                "state" : dics['state']
            }})

lons = []

#loads all longitudes to sort from west to east
for keys in states:
    lons.append(states[keys]['longitude'])

lons.sort(key = float)

points = []

#orders the dictionaries on westness
for west in lons:
    for keys in states:
        if states[keys]['longitude'] == west:
            points.append(states[keys])

geo = {
  "type": "FeatureCollection",
  "features": []
}

#creates the geojson file
for i in range(len(points)):
    #used to make sure colors don't repeat
    col = colors.pop()
    geo['features'].append(
        {
            "type": "Feature",
            "properties": {
                "marker-color": col,
                "marker-size": "medium",
                "marker-symbol": i + 1,
                "city": points[i]['city'],
                "growth": points[i]['growth'],
                "latitude": points[i]['latitude'],
                "longitude": points[i]['longitude'],
                "population": points[i]['population'],
                "state" : points[i]['state']
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    points[i]['longitude'],
                    points[i]['latitude']
                ]
            },
        }
    )

    #adds the lines to each city
    if i != len(points) - 1:
        geo['features'].append(
            {
                "type": "Feature",
                "properties": {
                    "stroke": col,
                    "stroke-width": 4,
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [points[i]['longitude'], points[i]['latitude']],
                        [points[i + 1]['longitude'], points[i + 1]['latitude']]
                    ]
                }
            }
        )
        
#writes results to file
f = open('Routes.geojson', 'w')
f.write(json.dumps(geo))