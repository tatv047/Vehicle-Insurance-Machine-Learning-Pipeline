import os 
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME,MONGODB_URL_KEY 

# load the crtificate authority file to avoid timeout errors when connecting to mongoDB
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to mongodb

    Attributes:
    ------------
    client: MongoClient
        A shared MongoClient instance for the class.
    database: Database
        The specific database instance that clinet connects to.

    Methods:
    ------------
    __init__(database_name: str) -> None:
        Initialises the MongoDB connection using the given database name.
    """
    client = None # shared MongoDBClient instance across all MongoDBClient instance.

    def __init__(self,database_name:str = DATABASE_NAME)-> None:
        """
        Initialises  a connection to the MongoDB database,if no exciting connection  is found,it establishes a new one.

        Parameters:
        -----------
        database_name: str,optional
            Name of the database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        ------------
        MyException
            If there is an issue connecting to MongoDB or if the environemnet variable for MongoDB URL isn't set.
        """
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment variable [{MONGODB_URL_KEY}] is not set.")

                #establish a new mongodb client
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile = ca)

            # use the shard mongodb client connection
            self.client = MongoDBClient.client
            self.database = self.client[database_name] # connect to the specified database
            self.database_name = database_name
            logging.info("MongoDB connection succesful") 
            
        except Exception as e:
            raise MyException(e,sys)
