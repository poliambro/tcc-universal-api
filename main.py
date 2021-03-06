import inits
from fastapi import FastAPI
from inits.init_dataset import dataset_completed
from fastapi.middleware.cors import CORSMiddleware
from routers import time_series, frequencies
from models.reviews import ReviewsCountByList, ReviewsGroupList
from models.attractions import ReviewsCountAttractionsByBranchList
from controllers import branches, attractions, utils


app = FastAPI()
app.include_router(time_series.router, tags=["Time series"])
app.include_router(frequencies.router, tags=["Frequencies"])

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/reviews/count/by/branch", response_model=ReviewsCountByList)
async def count_reviews_by_branch():
    by_branch = branches.get_reviews_count_by_branch(dataset_completed)
    return ReviewsCountByList(data=by_branch)


@app.get("/reviews/count/by/ratings", response_model=ReviewsGroupList)
async def count_reviews_by_ratings():
    by_ratings = utils.count_reviews_by(dataset_completed, "rating")
    return ReviewsGroupList(data=by_ratings)


@app.get("/reviews/count/by/year", response_model=ReviewsGroupList)
async def count_positive_reviews_by_year():
    reviews_by_year = utils.count_reviews_by(dataset_completed, "year")
    return ReviewsGroupList(data=reviews_by_year)


@app.get("/reviews/count/by/attraction", response_model=ReviewsCountAttractionsByBranchList)
async def reviews_count_by_attractions():
    by_attraction = attractions.count_reviews_by_attraction()
    return ReviewsCountAttractionsByBranchList(data=by_attraction)
