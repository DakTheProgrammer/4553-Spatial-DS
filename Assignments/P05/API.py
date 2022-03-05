from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

#helper class
from GeoHelper import Geo

#loads up API
if __name__ == '__main__':
    uvicorn.run("API:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)

app = FastAPI()
geo = Geo()

#root path goes to docs
@app.get('/')
async def root():
    return RedirectResponse(url="/docs")

#gets the most detailed polygon for a nation
@app.get('/poly/{country}')
async def poly(country: str):
    country = country.title()

    country = geo.getPoly(country)

    out = {'detail': 'Success','polygon': country}

    return out

#gets a list of countries
@app.get('/countries/')
async def countries():
    countries = geo.getCountries()

    out = {'detail': 'Success','countries': countries}

    return out

#gets a autofill like response for users when entering letters
@app.get('/autofill/{string}')
async def autofill(string: str):
    countries = geo.getCountries()

    result = []

    for cont in countries:
        if cont.lower().startswith(string):
            result.append(cont)

    out = {'detail': 'Success','countries': result}

    return out

#gets the centroid of a given nation
@app.get('/center/{country}')
async def center(country: str):
    country = country.title()

    country = geo.getPoly(country)

    center = geo.getCenterPoint(country)

    out = {'detail': 'Success','point': center}

    return out

#finds the distance between 2 polygons
#(NOTE DIDN'T DO DIFFERENCE IN 2 POINTS BC THE WAY IM SOLVING IT IS UNNECESSARY)
@app.get('/distance/{poly1}/{poly2}')
async def distance(poly1: str, poly2: str):
    poly1 = poly1.title()
    poly2 = poly2.title()

    poly1 = geo.reducePoints(poly1, .1)
    poly2 = geo.reducePoints(poly2, .1)

    distance = geo.getDistance(poly1, poly2)

    out = {'detail': 'Success','distance': distance}

    return out

#gets a hint of what continent a country is on
@app.get('/continent/{country}')
async def continent(country: str):
    out = {'detail': 'Success','continent': geo.getContinent(country.title())}

    return out