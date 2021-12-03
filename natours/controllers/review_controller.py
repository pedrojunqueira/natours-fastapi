from datetime import datetime

from fastapi.exceptions import HTTPException
from odmantic import ObjectId

from natours.models.database import engine as db
from natours.models.review_model import Review


async def get_reviews():
    reviews = await db.find(Review)
    return reviews


async def post_review(review):
    print(review)
    review = await db.save(review)
    print(review)
    return review

async def delete_review(Id):
    tour = await db.find_one(Review, Review.id == ObjectId(Id))
    if tour:
        await db.delete(tour)
    return tour
