import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
import nltk
from nltk.stem import PorterStemmer

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, convert, fetch_director, stem

@dataclass
class DataTransformationConfig:
    data_file_path:str = os.path.join("artifacts","data.csv")
    data_movie_file_path:str = os.path.join("artifacts","movie_data.csv")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(self, raw_data_path):
        try:
            data_df = pd.read_csv(raw_data_path)
            logging.info("Read train and test data successfully")

            dict_columns = ['genres', 'keywords',  'cast']
            para_columns = ['overview']
            director = ['crew']

            for col in dict_columns:
                data_df[col] = data_df[col].apply(convert)
                data_df[col] = data_df[col].apply(lambda x: [i.replace(" ", "") for i in x])

            nltk.download('punkt')
                
            for col in para_columns:
                data_df[col] = data_df[col].apply(lambda x: x.lower())
                data_df[col] = data_df[col].apply(stem)

            for col in director:
                data_df[col] = data_df[col].apply(fetch_director)
                data_df[col] = data_df[col].apply(lambda x: [i.replace(" ", "") for i in x])

            data_df['cast'] = data_df['cast'].apply(lambda x: x[:5])


            data_df['tags'] = data_df['overview'] + data_df['genres'] + data_df['keywords'] + data_df['cast'] + data_df['crew']
            data_df.rename(columns={'crew': 'director'}, inplace=True)

            new_df = data_df[['id', 'title', 'tags']]

            new_df.to_csv(self.data_transformation_config.data_file_path,index=False, header=True)
            data_df.to_csv(self.data_transformation_config.data_movie_file_path,index=False, header=True)

            logging.info("Saving the tranfoemations into a new file")

            return self.data_transformation_config.data_file_path
        
        except Exception as e:
            raise CustomException(e, sys)
