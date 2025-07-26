import json
import sys
from pandas import DataFrame
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.logger import logging
from src.entity.estimator import MyModel


class ProductionModelManager:
    """
    Manages saving/loading models and metrics to/from S3 and making predictions with production models.
    """

    def __init__(self, bucket_name: str, model_path: str, metric_path: str):
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.metric_path = metric_path
        self.s3 = SimpleStorageService()
        self.loaded_model: MyModel = None

    def is_model_present(self) -> bool:
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=self.model_path)
        except MyException as e:
            logging.warning(f"Model check failed: {e}")
            return False

    def is_metric_present(self) -> bool:
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=self.metric_path)
        except MyException as e:
            logging.warning(f"Metric check failed: {e}")
            return False

    def load_model(self) -> MyModel:
        """
        Load the model object from S3.
        """
        try:
            return self.s3.load_model(self.model_path, bucket_name=self.bucket_name)
        except Exception as e:
            raise MyException(e, sys)

    def load_metrics(self) -> dict:
        """
        Load the stored metrics JSON from S3.
        """
        try:
            file_obj = self.s3.get_file_object(filename=self.metric_path, bucket_name=self.bucket_name)
            content = self.s3.read_object(file_obj)
            metrics = json.loads(content)
            logging.info(f"Loaded metrics: {metrics}")
            return metrics
        except Exception as e:
            raise MyException(f"Failed to load metrics: {e}", sys)

    def get_f1_score(self) -> float:
        """
        Return F1 score from the metric artifact stored in S3.
        If not available, returns 0.0.
        """
        try:
            if not self.is_metric_present():
                logging.warning("metrics.json not found in S3. Assuming no previous model.")
                return 0.0
            return self.load_metrics().get("f1_score", 0.0)
        except Exception as e:
            logging.warning(f"Failed to extract F1 score from metrics: {e}")
            return 0.0

    def save_metrics(self, local_metrics_path: str, remove: bool = False) -> None:
        """
        Upload local metrics.json file to S3.
        """
        try:
            self.s3.upload_file(
                from_filename=local_metrics_path,
                to_filename=self.metric_path,
                bucket_name=self.bucket_name,
                remove=remove
            )
            logging.info(f"Uploaded metrics.json to s3://{self.bucket_name}/{self.metric_path}")
        except Exception as e:
            raise MyException(e, sys)

    def save_model(self, local_model_path: str, remove: bool = False) -> None:
        """
        Upload trained model to S3.
        """
        try:
            self.s3.upload_file(
                from_filename=local_model_path,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove
            )
            logging.info(f"Uploaded model to s3://{self.bucket_name}/{self.model_path}")
        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Predict on a given DataFrame using the loaded production model.
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e, sys)

    def save_model_and_metrics(self, model_path: str, metrics_path: str) -> None:
        """
        Convenience method to save both model and metrics in one call.
        """
        self.save_model(local_model_path=model_path)
        self.save_metrics(local_metrics_path=metrics_path)
