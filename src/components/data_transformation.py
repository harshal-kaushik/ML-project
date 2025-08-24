import  sys
from dataclasses import dataclass
import numpy as np
# doing all the feature encoding and any kind of feature engineering
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        try:
            numerical_features = ['reading score', 'writing score']
            categorical_features = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
            num_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='median', fill_value='missing')),
                                           ('scaler', StandardScaler(with_mean=True)),]

                                    )
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent', fill_value='missing')),
                ('OHE', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))
            ])
            logging.info("Numerical columns standardized")
            logging.info("categorical columns encoded")

            preprocessor = ColumnTransformer([
                ('num', num_pipeline, numerical_features),
                ('cat', cat_pipeline, categorical_features)
            ])

            return preprocessor
        except Exception as e :
            raise CustomException(e,sys)

    def initiate_data_transformer(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Training,Test data loaded")

            logging.info("obtaining preprocessor obj")
            preprocessor_obj = self.get_data_transformer_obj()

            target_column_name = 'math score'
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_train = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_test = test_df[target_column_name]
            logging.info("preprocessor obj created")
            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)


            train_arr = np.c_[input_feature_train_arr, target_train]
            test_arr = np.c_[input_feature_test_arr, target_test]
            logging.info('saved processed data')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            return train_arr, test_arr

        except Exception as e :
            raise CustomException(e,sys)
