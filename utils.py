import os
import random
import time

import numpy as np
import pandas as pd

def load_data(DATA_DIR, dataset):
    '''load the MovieLens 1m dataset in a Pandas dataframe'''
    if dataset == "ratings.dat":
        ratings = pd.read_csv(os.path.join(DATA_DIR, dataset), delimiter='::', header=None, 
            names=['UserID', 'Movie_ID', 'Rating', 'Timestamp'], engine='python')
        return ratings
    elif dataset == "movies.dat":
        movies = pd.read_csv(os.path.join(DATA_DIR, dataset), delimiter='::', header=None, 
            names=['MovieID', 'Title', 'Genres'], engine='python', encoding='latin-1')
        return movies
    elif dataset == "users.dat":
        users = pd.read_csv(os.path.join(DATA_DIR, dataset), delimiter='::', header=None, 
            names=['UserID','Gender','Age','Occupation','Zip-code'], engine='python')
        return users