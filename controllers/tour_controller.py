from pathlib import Path
import os
import json

from models.tour_model import Tour

p = Path(os.path.dirname(__file__)).resolve()

with open(p / "../dev-data/data/tours-simple.json", "r") as fp:
    tours = json.load(fp)


def get_tours():
    with open(p / "../dev-data/data/tours-simple.json", "r") as fp:
        tours = json.load(fp)
    return tours


def post(tour):
    #new_tour = {"name": "Hicker", "rating": 4.5, "price": 455}
    t = Tour(**tour.dict())
    t.save()
    return tour


def get_tour(Id):
    tours = get_tours()
    tour = list(filter(lambda t: t["id"] == Id, tours))
    return tour


def patch_tour(Id):
    pass


def delete_tour(Id):
    pass
