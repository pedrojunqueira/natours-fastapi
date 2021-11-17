from odmantic import ObjectId

from models.tour_model import Tours
from models.database import engine as db


async def get_tours():
    tours = await db.find(Tours)
    return tours


async def post(tour):
    tour = await db.save(tour)
    return tour.dict()


async def get_tour(Id):
    tour = await db.find_one(Tours, Tours.id == ObjectId(Id))
    return tour


async def patch_tour(Id, new_tour):
    tour = await db.find_one(Tours, Tours.id == ObjectId(Id))
    if validate_patch_body(new_tour, tour):
        for k, v in new_tour.items():
            if k != "id":
                setattr(tour, k, v)
        await db.save(tour)
        return tour
    return None


async def delete_tour(Id):
    tour = await db.find_one(Tours, Tours.id == ObjectId(Id))
    await db.delete(tour)
    return tour


def validate_patch_body(patch, model):
    keys = patch.keys()
    model_keys = model.dict()
    return all(k in model_keys for k in keys)
