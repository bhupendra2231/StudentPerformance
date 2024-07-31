import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts","prerprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transforamtion_config=DataTransformationConfig()
    def get_data_transformer_object(self):
        """
        This function is reponsible for data transformation
        """
        try:
            numerical_columns=["writing_score","reading_score"]
            categorical_col=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("StandardScaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("OneHotEncoder",OneHotEncoder(handle_unknown='ignore')),
                    ("scaler",StandardScaler(with_mean=False))

                ]
            )
            logging.info("numerical columns scaling completed")
            logging.info("categorical columns encoding completed")
            
            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_col)
                ]
            )
            return preprocessor
            
        except Exception as e :
            raise CustomException(e,sys)
    
    def intiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read train and test data compeleted")
            logging.info("obtaining preprocessing object")
            preprocessor_obj=self.get_data_transformer_object()
            target_column="math_score"
            numerical_columns=["writing_score","reading_score"]
            input_feature_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]
            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]
            logging.info("Appying preprocessing obejct on training datatframe and testing dataframe")
            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)
            train_arr=np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr=np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]
            logging.info("Saved preprocessing object")
            save_object(
                file_path=self.data_transforamtion_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transforamtion_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)
