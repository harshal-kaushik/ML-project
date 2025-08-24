import os
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,GradientBoostingRegressor)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_model

@dataclass
class ModelTrainerConfig:
    train_model_file_path=os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Initiating model trainer")
            logging.info("Split train and test array")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models = {
                "Random forest regressor": RandomForestRegressor(),
                "Gradient boosting regressor": GradientBoostingRegressor(),
                "Linear regression": LinearRegression(),
                "KNN regressor": KNeighborsRegressor(),
                "Decision tree regressor": DecisionTreeRegressor(),
                "Adaboost regressor": AdaBoostRegressor(),
                "Xgboost regressor": XGBRegressor(),
                "Catboost regressor": CatBoostRegressor(),


            }
            model_report : dict = evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)
            # 1. Get the highest score from the report
            best_model_score = max(model_report.values())

            # 2. Correctly get the NAME of the model that produced the highest score
            best_model_name = max(model_report, key=model_report.get)

            # 3. Get the actual model object from the 'models' dictionary
            best_model = models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info("Best model found")

            save_object(
                file_path=self.model_trainer_config.train_model_file_path,
                obj=best_model
            )
            predictions = best_model.predict(X_test)
            r2 = r2_score(y_test, predictions)
            return r2



        except Exception as e:
            raise CustomException(e,sys)



