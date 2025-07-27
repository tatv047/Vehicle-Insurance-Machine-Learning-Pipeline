# # below code is to check the logging config
# # from src.logger import logging

# # logging.debug("This is a debug message.")
# # logging.info("This is an info message.")
# # logging.warning("This is a warning message.")
# # logging.error("This is an error message.")
# # logging.critical("This is a critical message.")


# # below code is to check the exception config
# # from src.logger import logging
# # from src.exception import MyException
# # import sys

# # try:
# #     a = 1+'Z'
# # except Exception as e:
# #     logging.info(e)
# #     raise MyException(e, sys) from e

# #--------------------------------------------------

# from src.pipeline.training_pipeline import TrainingPipeline

# pipeline = TrainingPipeline()
# pipeline.run_pipeline()

# from src.pipeline.prediction_pipeline import VehicleData,VehicleDataClassifier

# vehicle_data = VehicleData.get_vehicle_input_data_frame()
# model_predictor = VehicleDataClassifier()
# value = model_predictor.predict(dataframe=vehicle_data)

# from fastapi import FastAPI,HTTPException
# from pydantic import BaseModel 

# app = FastAPI()

# # In memory data base
# items_db = {
#     1: {"name":"Book","price":299},
#     2: {"name":"Pen","price":20}
# }

# # Pydantic model for item output
# class Item(BaseModel):
#     name:str
#     price: float 

# # GET all items
# @app.get("/items")
# def get_items():
#     return items_db

# #GET one item by id
# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     item = items_db.get(item_id)
#     if item is None:
#         raise HTTPException(status_code = 404,detail = "Item not found")
#     return item

# # POST: add a new item
# @app.post("/items")
# def create_item(item: Item):
#     new_id = max(items_db.keys(),default=0) + 1
#     items_db[new_id] = item.dict()
#     return {"id": new_id,"item": item}



# # @app.get("/")
# # def read_root():
# #     return {"message":"hello!, FastAPI"}

# # @app.get("/greet/{name}")
# # def greet_user(name:str):
# #     return {"greeting": f"Hello, {name}!!" }

import os
user_id = os.getenv("AWS_USER_ID")
bucket_name = user_id + "-my-model-mlops-proj"
print(user_id)
print(type(user_id))
print(bucket_name)
print(type(bucket_name))