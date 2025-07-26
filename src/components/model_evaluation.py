from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact, ModelEvaluationArtifact
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_object
from src.entity.s3_manager import ProductionModelManager 
from dataclasses import dataclass
from typing import Optional
import sys


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: Optional[float]
    is_model_accepted: bool
    difference: float


class ModelEvaluation:
    def __init__(self,
                 model_evaluation_config: ModelEvaluationConfig,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact

            # Initialize the production model manager (merged logic for model & metric)
            self.production_model_mgr = ProductionModelManager(
                bucket_name=self.model_evaluation_config.bucket_name,
                model_path=self.model_evaluation_config.s3_model_key_path,
                metric_path=self.model_evaluation_config.s3_metric_key_path
            )
        except Exception as e:
            raise MyException(e, sys) from e

    def get_production_model_metrics(self) -> Optional[float]:
        """
        Retrieves the stored F1 score of the production model from S3.
        Returns None if no metrics are found.
        """
        try:
            f1_score_val = self.production_model_mgr.get_f1_score()

            if f1_score_val == 0.0:
                logging.info("Production model F1 score is 0.0 or missing. Assuming first run.")
                return None

            return f1_score_val

        except Exception as e:
            raise MyException(e,sys)

    def evaluate_model(self) -> EvaluateModelResponse:
        """
        Compares the trained model's F1 score with the production model's F1 score.
        Returns an evaluation response indicating if the new model is better.
        """
        try:
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            logging.info(f"Trained model F1 score: {trained_model_f1_score}")

            best_model_f1_score = self.get_production_model_metrics()

            if best_model_f1_score is None:
                logging.info("No production model metrics found — assuming first run.")
                tmp_best_model_score = 0.0
            else:
                tmp_best_model_score = best_model_f1_score

            is_model_accepted = trained_model_f1_score > tmp_best_model_score
            diff = trained_model_f1_score - tmp_best_model_score

            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=is_model_accepted,
                difference=diff
            )

            logging.info(f"Model evaluation result: {result}")
            return result

        except Exception as e:
            raise MyException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """
        Initiates model evaluation and creates the corresponding artifact.
        """
        try:
            print("------------------------------------------------------------------------------------------------")
            logging.info("Initialized Model Evaluation Component.")
            evaluate_model_response = self.evaluate_model()

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                s3_model_path=self.model_evaluation_config.s3_model_key_path,
                s3_metric_path=self.model_evaluation_config.s3_metric_key_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                metric_file_path = self.model_trainer_artifact.metric_file_path,
                changed_metric=evaluate_model_response.difference
            )

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact

        except Exception as e:
            raise MyException(e, sys) from e
