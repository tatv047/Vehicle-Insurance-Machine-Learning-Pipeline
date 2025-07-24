import os 
import sys 

from src.exception import MyException
from src.logger import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.proj_data import ProjData

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig= DataIngestionConfig()):
        """
        data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data_into_feature_store(self)-> DataFrame:
        """
        Method name: export_data_into_feature_store
        Description: exports data from mongoDB to csv files

        Output: data is returned as artifact of data ingestion component
        On Failure: Write an exception log and raise an exception
        """
        try:
            logging.info("Exporting data from mongoDB...")
            data = ProjData()
            dataframe  = data.export_collection_as_dataframe(collection_name=DataIngestionConfig.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into fetaure store file path:{feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise MyException(e,sys)


    def split_data_as_train_test(self,dataframe: DataFrame)-> None:
        """
        Method name: split_data_as_train_test
        Description: splits dataframe into train and test sets in the given split ratio

        Output: Train and test CSVs are saved to local filesystem.
        On Failure: Write an exception log and raise an exception
        """
        logging.info("Entered split_data_as_train_test method of 'DataIngestion' class...")

        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train_test_split on the dataframe")
            train_dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_dir_path,exist_ok=True)

            test_dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(test_dir_path,exist_ok=True)

            logging.info("Exporting train and test file path..")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index = False,header = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index = False,header = True)

            logging.info("Exported train and test file path !!!")
            logging.info(
                "Exited split_data_as_train_test method of DataIngestion class"
            )
        except Exception as e:
            raise MyException(e,sys)
        
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        """
        Method name: initiate_data_ingestion
        Description: initiates the data ingestion components of training pipeline

        Output: Train and test sets are returned as the artifacts of data ingestion components
        On Failure: Write an exception log and raise an exception
        """
        logging.info("Entered initiate_data_ingestion method of the DataIngestion class")
        try:
            dataframe = self.export_data_into_feature_store()

            logging.info("Got the data from MongoDB")
            
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise MyException(e,sys)
