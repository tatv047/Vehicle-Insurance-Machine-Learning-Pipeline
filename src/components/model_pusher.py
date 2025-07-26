import sys
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_manager import ProductionModelManager 


class ModelPusher:
    def __init__(self,
                 model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference of model evaluation stage
        :param model_pusher_config: Configuration for model pusher
        """
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config

        # model & metric handler
        self.prod_manager = ProductionModelManager(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path,
            metric_path=model_pusher_config.s3_metric_key_path
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Pushes the trained model and metrics to S3 only if model is accepted.
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            print("------------------------------------------------------------------------------------------------")
            if not self.model_evaluation_artifact.is_model_accepted:
                logging.info("Model is not accepted. Skipping model push to S3.")
                return ModelPusherArtifact(
                    bucket_name=self.model_pusher_config.bucket_name,
                    s3_model_path=None,
                    s3_metric_path=None
                )

            logging.info("Model accepted. Proceeding to push model and metrics to S3.")

            # Push trained model
            self.prod_manager.save_model_and_metrics(
                model_path=self.model_evaluation_artifact.trained_model_path,
                metrics_path=self.model_evaluation_artifact.metric_file_path
            )

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path,
                s3_metric_path=self.model_pusher_config.s3_metric_key_path
            )

            logging.info(f"Model pusher artifact created: {model_pusher_artifact}")
            return model_pusher_artifact

        except Exception as e:
            raise MyException(e, sys) from e
