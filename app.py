from pathlib import Path
import os
import json

from fastapi import FastAPI, Response, status


app = FastAPI()


p = Path(os.path.dirname(__file__)).resolve()

with open( p / "dev-data/data/tours-simple.json", "r" ) as fp:
    tours = json.load(fp)


@app.get('/api/v1/tours')
async def get_all_tours():
    return {
        "status" : 'success',
        "results" : len(tours),
        "data" : tours,
    }

@app.get('/api/v1/tours/{id:int}')
async def get_tour(id:int, response:Response):
    tour = list(filter(lambda t: t["id"]==id, tours))
    if tour:
        return {
            "status" : 'success',
            "data" : tour[0],
        }
    if not tour:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": 'fail', "message": 'Invalid Id' }

@app.post('/api/v1/tours')
async def create_tour(tour:dict):
    newId = tours[-1]["id"] +1
    tour["id"] = newId
    tours.append(tour)
    with open( p / "dev-data/data/tours-simple.json", "w+" ) as fp:
        json.dump(tours, fp)
    return {
        "status": 'success',
        "data": {
          "tour": tour,
        } 
    }

@app.patch('/api/v1/tours/{id:int}')
async def update_tour(id:int):
    return {
        "status" : 'success',
        "data" : None,
    }

@app.delete('/api/v1/tours/{id:int}')
async def delete_tour(id:int):
    return {
        "status" : 'success',
        "data" : None,
    }
