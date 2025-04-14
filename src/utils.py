import os
import sys

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from nltk.stem import PorterStemmer
import ast
import pickle


from src.exception import CustomException
from src.logger import logging


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
  
    except Exception as e:
        raise CustomException(e, sys)
    
def convert(obj):
    try:
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    except Exception as e:
        raise CustomException(e, sys)
    
def fetch_director(obj):
    try:
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L
    
    except Exception as e:
        raise CustomException(e, sys)
    
def stem(text):
    try:
        ps = PorterStemmer()
        y = []
        for i in text.split():
            y.append(ps.stem(i))
        return y
    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)