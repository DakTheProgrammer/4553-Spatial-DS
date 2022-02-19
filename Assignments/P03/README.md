## P03
### Dakota Wilson
### Description:

Creates a Voronoi diagram of all major cities. With this it then places all of the polygons in a rtree combined with all of the points of UFO sightings in the US. The rtree is the queried to find all of the points in all of the polygons. With that info it then writes to a JSON file the polygons and all of the points of UFOs in a given polygon.

### Files

|   #   | File                                                                                                                                | Description                                                 |
| :---: | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
|   1   | [main.py](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P03/main.py)                                    | Main file that process all data and makes JSON files        |
|   2   | [cities.geojson](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P03/cities.geojson)                      | File with major cities                                      |
|   3   | [ufo_data.csv](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P03/ufo_data.csv)                          | File that contains ufo sightings                            |
|   4   | [FixCSV.py](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P03/FixCSV.py)                                | File that makes a csv that has only American ufo sightings  |
|   5   | [BetterUFOData.csv](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P03/BetterUFOData.csv)                | File that has only American ufo sightings                   |
|   6   | [PointsInPolys.json](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P03/PointsInPolys.json)              | File that stores the output of all polygons                 |
|   7   | [us_border_shp](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P03/us_border_shp)                        | Folder used to make shapes on a map                         |


### Instructions

- run main.py and watch the magic
- run FixCSV.py to generate a better CSV for American UFO sightings

- Example Command:
    - `python main.py`
    - `python FixCSV.py`