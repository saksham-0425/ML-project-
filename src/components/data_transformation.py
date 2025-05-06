import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer  #used to do one hot encoding

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer_object(self):
        # "this function is used for data transformation i.e handling numerical and categorical features"
        try:
            numerical_features=['writing score','reading score']
            categorical_features=['gender','race/ethnicity','parental level of education','lunch','test preparation course']
            
            # pipelines are sequences of connected operations that process data, typically for tasks like data preprocessing, machine learning, or data analysis
            num_pipeline=Pipeline(
                steps=[("imputer",SimpleImputer(strategy="median")), #imputer is used to fill the missing values in the dataset
                        ("scaler",StandardScaler())] #standard scaler is used to scale the data to a standard normal distribution
            )
            
            cat_pipelines=Pipeline(
                steps=[("imputer",SimpleImputer(strategy="most_frequent")),    #imputer is used to fill the missing values in the dataset]
                        ("onehotencoder",OneHotEncoder()), #one hot encoder is used to convert categorical data into numerical data
                        ("scaler",StandardScaler(with_mean=False))] #standard scaler is used to scale the data to a standard normal distribution
            )
            
            logging.info("Numerical columns standard scaling completed")
            logging.info("Categorical columns standard scaling completed")
            
            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_features), #pipeline for numerical features
                    ("cat_pipeline",cat_pipelines,categorical_features) #pipeline for categorical features
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
     try:
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)

        logging.info("Read train and test data completed")
        logging.info("Obtaining preprocessing object")

        preprocessor_obj = self.get_data_transformer_object()
        target_column_name = 'math score'

        input_features_train_df = train_df.drop(columns=[target_column_name], axis=1)
        target_feature_train_df = train_df[target_column_name]

        input_features_test_df = test_df.drop(columns=[target_column_name], axis=1)
        target_feature_test_df = test_df[target_column_name]

        logging.info("Applying preprocessing object on training dataframe and test dataframe")
        input_feature_train_arr = preprocessor_obj.fit_transform(input_features_train_df)
        input_feature_test_arr = preprocessor_obj.transform(input_features_test_df)

        train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
        test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

        logging.info("Saved preprocessing object")

        save_object(
            file_path=self.data_transformation_config.preprocessor_obj_file_path,
            obj=preprocessor_obj
        )

        return (train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path)

     except Exception as e:
        raise CustomException(e, sys)

                
                
                
    
