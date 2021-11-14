from pathlib import Path
import os
import json


p = Path(os.path.dirname(__file__)).resolve()

with open(p / "../dev-data/data/tours-simple.json", "r") as fp:
    tours = json.load(fp)


def get_tours():
    with open(p / "../dev-data/data/tours-simple.json", "r") as fp:
        tours = json.load(fp)
    return tours


def post(tour):
    tours = get_tours()
    newId = tours[-1]["id"] + 1
    tours = get_tours()
    tour["id"] = newId
    tours.append(tour)
    with open(p / "../dev-data/data/tours-simple.json", "w+") as fp:
        json.dump(tours, fp)
    return tour


def get_tour(Id):
    tours = get_tours()
    tour = list(filter(lambda t: t["id"] == Id, tours))
    return tour


def patch_tour(Id):
    pass


def delete_tour(Id):
    pass
