import pandas as pd
import os


dataset_completed = pd.read_csv(os.path.join("./dataset", "dataset_completed.csv"))
dataset_with_attractions = pd.read_csv(os.path.join("./dataset", "dataset_completed_attractions.csv"))
dataset_attractions_count = pd.read_csv(os.path.join("./dataset", "dataset_attractions_count.csv"))
