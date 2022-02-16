## P02
### Dakota Wilson
### Description:

Finds the distance to all other cities from program 1 and loads that information into a JSON file. Uses a csv file to help find the average distance of the 100 closest ufos from each city and writes that to a JSON file for later use. I did the JSON format for the distances so that I can easily go through each city and also so I could store a sorted list so the top elements would be closest to the top when finding best path. I also chose json for the UFO distances so that I could easily have the location of each city with coordinates as well as having the distances at the same spot so that drawing the Voronoi Diagram would be a lot easier.

### Files

|   #   | File                                                                                                                                | Description                                                 |
| :---: | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
|   1   | [Main.py](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P02/main.py)                                    | Main file that process all data and makes JSON files        |
|   2   | [cities.geojson](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P02/cities.geojson)                      | File with major cities                                      |
|   3   | [ufo_data.csv](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P02/ufo_data.csv)                          | File that contains ufo sightings                            |
|   4   | [distances.json](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P02/distances.json)                      | File that has all the distances from each major city        |
|   5   | [average_ufo.json](https://github.com/DakTheProgrammer/4553-Spatial-DS/blob/main/Assignments/P02/average_ufo.json)                  | File that has the average distance to the 100 closets ufos  |


### Instructions

- run main.py and watch the magic

- Example Command:
    - `python main.py`