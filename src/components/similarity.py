import os
import sys
import pandas as pd
import numpy as np
import pickle
from dataclasses import dataclass

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class SimilarityConfig:
    similarity_file_path: str = os.path.join("artifacts", "similarity.pkl")

class Similarity:
    def __init__(self):
        self.similarity_config = SimilarityConfig()

    def initiate_similarity(self, data_file_path):
        try:
            data_df = pd.read_csv(data_file_path)

            cv = CountVectorizer(max_features=10000, stop_words='english')
            vectors = cv.fit_transform(data_df['tags']).toarray()

            similarity = cosine_similarity(vectors)

            pickle.dump(similarity, open(self.similarity_config.similarity_file_path, 'wb'))



            logging.info("Similarity matrix saved successfully.")
            return similarity
            
        except Exception as e:
            raise CustomException(e, sys)
            
