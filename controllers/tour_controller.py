from datetime import datetime
from fastapi.exceptions import HTTPException
from odmantic import ObjectId

from models.tour_model import Tours
from models.database import engine as db


def query_params(query):
    sort_by = (
        query.get("sort").split(",") if query.get("sort") else Tours.createdAt.desc()
    )
    sort_by = (
        tuple([getattr(Tours, atr) for atr in sort_by])
        if sort_by
        else Tours.createdAt.desc()
    )
    limit = int(query.get("limit")) if query.get("limit") else None
    page = int(query.get("page")) if query.get("page") else None
    skip = (page - 1) if page else 0
    return sort_by, skip, limit


async def get_tours(query):
    sort_by, skip, limit = query_params(query)
    tours = await db.find(Tours, sort=sort_by, skip=skip, limit=limit)
    return tours


async def post(tour):
    tour = await db.save(tour)
    return tour.dict()


async def get_tour(Id):
    tour = await db.find_one(Tours, Tours.id == ObjectId(Id))
    return tour


async def patch_tour(Id, new_tour):
    tour = await db.find_one(Tours, Tours.id == ObjectId(Id))
    if tour:
        if validate_patch_body(new_tour, tour):
            for k, v in new_tour.items():
                if k != "id":
                    setattr(tour, k, v)
            await db.save(tour)
    return tour


async def delete_tour(Id):
    tour = await db.find_one(Tours, Tours.id == ObjectId(Id))
    if tour:
        await db.delete(tour)
    return tour


def validate_patch_body(patch, model):
    keys = patch.keys()
    model_keys = model.dict()
    return all(k in model_keys for k in keys)


async def tour_stats():
    tours = db.get_collection(Tours)
    stats = await tours.aggregate(
        [
            {
                "$match": {"ratingsAverage": {"$gte": 4.5}},
            },
            {
                "$group": {
                    "_id": {"$toUpper": "$difficulty"},
                    "numTours": {"$sum": 1},
                    "numRatings": {"$sum": "$ratingsQuantity"},
                    "avgRating": {"$avg": "$ratingsAverage"},
                    "avgPrice": {"$avg": "$price"},
                    "minPrice": {"$min": "$price"},
                    "maxPrice": {"$max": "$price"},
                },
            },
            {
                "$sort": {"avgPrice": 1},
            },
        ]
    ).to_list(length=None)
    return stats


async def get_monthly_plan(year):
    if year > 9999:
        raise HTTPException(404, f"{year} is not a valid year range")
    tours = db.get_collection(Tours)
    plan = await tours.aggregate(
        [
            {
                "$unwind": "$startDates",
            },
            {
                "$match": {
                    "startDates": {
                        "$gte": datetime(year, 1, 1),
                        "$lte": datetime(year, 12, 31),
                    },
                },
            },
            {
                "$group": {
                    "_id": {"$month": "$startDates"},
                    "numTourStarts": {"$sum": 1},
                    "tours": {"$push": "$name"},
                },
            },
            {
                "$addFields": {"month": "$_id"},
            },
            {
                "$project": {
                    "_id": 0,
                },
            },
            {
                "$sort": {"numTourStarts": -1},
            },
            {
                "$limit": 12,
            },
        ]
    ).to_list(length=None)
    return plan
