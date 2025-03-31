import sys
import os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COULUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import DataTransforamtionArtifact, DataValidationArtifact

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransforamtionArtifact = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        It initiates a KNNImputer object with the parameters specified in the training_pipeline.py file
          and returns a Pipeline object with the KNNImputer object as the first step.
        
        Args:
            cls: DataTransformation

        Returns:
            A Pipeline object
        """
        logging.info("Entered get_data_transformer_object method of Transformation Class")

        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)#在 Python 中，** 运算符用于字典解包（dictionary unpacking）。它的功能是将一个字典作为关键字参数传递给函数或方法。
            logging.info(f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
        
    def initiate_data_transformation(self)->DataTransforamtionArtifact:
        logging.info("Entered initiate_data_transformation of DataTransformation class")
        try:
            logging.info("Starting data Transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## training dataframe
            # Drop _id column and other non-numeric columns if present
            if '_id' in train_df.columns:
                train_df = train_df.drop(columns=['_id'], axis=1)
            if '_id' in test_df.columns:
                test_df = test_df.drop(columns=['_id'], axis=1)
                
            input_feature_train_df = train_df.drop(columns = [TARGET_COULUMN], axis = 1 )
            target_feature_train_df = train_df[TARGET_COULUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)


            ## testing dataframe

            input_feature_test_df = test_df.drop(columns = [TARGET_COULUMN], axis = 1 )
            target_feature_test_df = test_df[TARGET_COULUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)# 训练（学习转换规则）
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)# # 应用转换到训练集
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array = test_arr,)

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            # preparing object

            data_transformation_artifact = DataTransforamtionArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
