from models.branches import ReviewsCountByBranch
from models.by_year import ReviewsCountByYear
from models.ratings import ReviewsCountByRating
import pandas as pd
from autots import AutoTS
import matplotlib.pyplot as plt
import os

my_path = os.path.relpath(os.path.join(os.path.dirname(__file__), os.pardir))


def count_reviews_by_year(grouped_df):
    list_by_year = []
    for key, item in grouped_df:
        count_by_year = ReviewsCountByYear(year=str(key), count=len(item))
        list_by_year.append(count_by_year)
    return list_by_year


def count_reviews_by_branch(grouped_df):
    list_by_branch = []
    for key, item in grouped_df:
        count_by_branch = ReviewsCountByBranch(branch=key, count=len(item))
        list_by_branch.append(count_by_branch)
    return list_by_branch


def count_reviews_by_rating(grouped_df):
    list_by_rating = []
    for key, item in grouped_df:
        count_by_rating = ReviewsCountByRating(rating=key, count=len(item))
        list_by_rating.append(count_by_rating)
    return list_by_rating


def parse_df(dataset):
    """Parse the dataset to the expected output to autoTs models"""
    grouped_ds = dataset.groupby(["year", "month"])
    parsed_df = pd.DataFrame(columns=["date", "reviews_count"])
    for key, item in grouped_ds:
        parsed_df = parsed_df.append({"date": f'{key[0]}-{key[1]}', "reviews_count": len(item)}, ignore_index=True)

    parsed_df['date'] = pd.to_datetime(parsed_df['date'], infer_datetime_format=True, format='%y%m')
    parsed_df['reviews_count'] = pd.to_numeric(parsed_df["reviews_count"])
    parsed_df = parsed_df[["date", "reviews_count"]]
    parsed_df["date"] = pd.to_datetime(parsed_df.date)
    return parsed_df


def get_indexed_dataframe(df):
    return df.set_index('date')


def train_and_predict(df):
    model = AutoTS(forecast_length=30, frequency='infer',
                   ensemble='simple', drop_data_older_than_periods=100)
    model = model.fit(df, date_col='date', value_col='reviews_count', id_col=None)
    prediction = model.predict()
    forecast = prediction.forecast
    return forecast


def plot_prediction(df, file_name, fig_number):
    forecast = train_and_predict(df)
    temp_df = get_indexed_dataframe(df)
    plt.figure(fig_number)
    temp_df['reviews_count'].plot(figsize=(12, 8), title='Reviews Count Over the Years', fontsize=20, label='Train')
    forecast['reviews_count'].plot(figsize=(12, 8), title='Reviews Count Over the Years', fontsize=20, label='Test')
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join("./assets", file_name))

