import os
import sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.similarity import SimilarityConfig, Similarity

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path:str =  os.path.join("artifacts","merged_data.csv")



class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            credits=pd.read_csv("notebook/Dataset/tmdb_5000_credits.csv")
            movies=pd.read_csv("notebook/Dataset/tmdb_5000_movies.csv")
            movies=movies.merge(credits, on='title')
            logging.info("Read the data successfully")

            logging.info("Dropping the columns which are not required")
            features = ['id', 'title', 'genres', 'keywords', 'overview', 'cast', 'crew']
            movies = movies[features]

            logging.info("Removing missing rows")
            movies.dropna(inplace=True)

            movies.to_csv(self.ingestion_config.raw_data_path,index=False, header=True)

            logging.info("Ingestion of the data is completed")
            logging.info("the path is"+ str(self.ingestion_config.raw_data_path))

            return self.ingestion_config.raw_data_path
        
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    obj = DataIngestion()
    raw_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_file_path= data_transformation.initiate_data_transformation(raw_data_path)
    
    modelTrainer = Similarity()
    print(modelTrainer.initiate_similarity(data_file_path))
