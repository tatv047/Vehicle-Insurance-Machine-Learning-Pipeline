import sys 
import pandas as pd 
import numpy as np 
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException

class ProjData:
    """
    A class to export MongoDB records as a pandas Dataframe
    """
    def __init__(self)-> None:
        """
        Initialises the mongodb client connection
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e,sys)
        
    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str] = None)->pd.DataFrame:
        """
        Exports an entire MongoDB collection as a dataframe

        Parameters:
        -----------
        collection_name: str
            name of the collection
        database_name: Optional[str]
            Name of the database(optional).Defaults to DATABASE_NAME

        Returns:
        -----------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            # Access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                colection = self.mongo_client[database_name][collection_name]
            
            # convert collection to dataframe
            print("Fetching data from MongoDB ...")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fetched wiith len: {len(df)}")
            if "_id" in df.columns.to_list():
                df = df.drop(columns=['_id'],axis=1)
            df.replace({'na':np.nan},inplace=True)
            return df

            
        except Exception as e:
            raise MyException(e,sys)
