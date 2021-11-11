from pathlib import Path
import os
import json
import time

from fastapi import FastAPI, Response, status, Request


app = FastAPI()


p = Path(os.path.dirname(__file__)).resolve()

with open( p / "dev-data/data/tours-simple.json", "r" ) as fp:
    tours = json.load(fp)


# added midddleware

@app.middleware("http")
async def add_some_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(process_time)
    return response


@app.get('/api/v1/tours')
async def get_all_tours():
    return {
        "status" : 'success',
        "results" : len(tours),
        "data" : tours,
    }


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

@app.get('/api/v1/users')
async def get_all_users():
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }


@app.post('/api/v1/users')
async def create_user(tour:dict):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }

@app.get('/api/v1/users/{id:int}')
async def get_user(id:int):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }


@app.patch('/api/v1/users/{id:int}')
async def update_user(id:int):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }

@app.delete('/api/v1/users/{id:int}')
async def delete_user(id:int):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }
