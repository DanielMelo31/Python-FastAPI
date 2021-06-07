from typing import AsyncIterable, List
from fastapi import APIRouter, HTTPException
from ..database import database_connection
from ..models import *
from ..schemas import *

route = APIRouter(prefix='/api/v1/review')
# ---------------Review---------------

# Create new review
@route.post('/reviews', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if Movie.select().where(Movie.id == user_review.movies_id).first() is None:
        raise HTTPException(status_code=404, detail='Movie not found')

    # Creating a new review in DB
    user_review = UserReview.create(
        user_id= user_review.user_id,
        movies_id = user_review.movies_id,
        review = user_review.review,
        score = user_review.score
    )

    # Return an ReviewResponseModel object
    return user_review

# Get a review paginated
@route.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int=1, limit: int=10):
    # SELECT * FROM user_review
    review = UserReview.select().paginate(page, limit)

    return [user_review for user_review in review]


# et a review by Id
@route.get('{review_id}', response_model=ReviewResponseModel)
async def get_review_id(review_id: int):
    # .first return the first object that fit the search
    response = UserReview.select().where(UserReview.id == review_id).first()

    if response is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return response


# Update a value
@route.put('{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, user_review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    user_review.review = user_review_request.review
    user_review.score = user_review_request.score

    user_review.save()

    return user_review


# Delete a value
@route.delete('{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review not found')

    user_review.delete_instance()

    return user_review
