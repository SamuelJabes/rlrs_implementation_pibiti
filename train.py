#Dependencies
import pandas as pd
import numpy as np
import tensorflow as tf
import itertools
import matplotlib.pyplot as plt
import time
from datetime import datetime

from env import Env
from recommender import DRRAgent

import os
DATA_DIR = 'data'
STATE_SIZE = 5
MAX_EPISODE_NUM = 8000

# os.environ["CUDA_VISIBLE_DEVICES"]="1"

if __name__ == "__main__":

    print('Data loading...')

    #Loading datasets
    ratings_list = [i.strip().split("::") for i in open(os.path.join(DATA_DIR,'ratings.dat'), 'r').readlines()]
    ratings_list = [
    [int(row[0]), int(row[1]), int(row[2]), int(row[3])]  # Converter cada string para int
    for row in ratings_list
    ]
    users_list = [i.strip().split("::") for i in open(os.path.join(DATA_DIR,'users.dat'), 'r').readlines()]
    movies_list = [i.strip().split("::") for i in open(os.path.join(DATA_DIR,'movies.dat'),encoding='latin-1').readlines()]
    ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'MovieID', 'Rating', 'Timestamp'], dtype = np.uint32)
    movies_df = pd.DataFrame(movies_list, columns = ['MovieID', 'Title', 'Genres'])
    movies_df['MovieID'] = movies_df['MovieID'].apply(pd.to_numeric)

    print("Data loading complete!")
    print("Data preprocessing...")

    # 영화 id를 영화 제목으로
    movies_id_to_movies = {movie[0]: movie[1:] for movie in movies_list}
    ratings_df = ratings_df.map(int)

    # 유저별로 본 영화들 순서대로 정리
    users_dict = np.load('./data/user_dict.npy', allow_pickle=True)

    # 각 유저별 영화 히스토리 길이
    users_history_lens = np.load('./data/users_histroy_len.npy')

    # get the number of users and items
    users_num = max(ratings_df["UserID"])
    items_num = len(movies_df)

    # Training setting
    train_users_num = int(users_num * 0.8)
    train_items_num = items_num
    train_users_dict = {k:users_dict.item().get(k) for k in range(1, train_users_num+1)}
    train_users_history_lens = users_history_lens[:train_users_num]
    
    print('DONE!')
    time.sleep(2)

    env = Env(train_users_dict, train_users_history_lens, movies_id_to_movies, STATE_SIZE)
    recommender = DRRAgent(env, users_num, items_num, STATE_SIZE, use_wandb=False)
    recommender.actor.build_networks()
    recommender.critic.build_networks()
    
    save_model_weight_dir = f"./save_model/trail-{datetime.now().strftime('%Y-%m-%d-%H')}"
    if not os.path.exists(save_model_weight_dir):
        os.makedirs(os.path.join(save_model_weight_dir, 'images'))
        
    recommender.train(MAX_EPISODE_NUM, save_model_weight_dir, load_model=False)