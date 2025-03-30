from provider.mlflow_provider import MLFlowProvider
from shared.dto.forecast_result import ForecastResult
from shared.view.request_view import ForecastRequest
import pandas as pd


class ForecastService:
    """A service for forecasting item sales.

    Args:
        mlflow_provider: A client for an MLFlow Model which will produce the forecast.
    """

    def __init__(self, mlflow_provider: MLFlowProvider):
        self.mlflow_provider = mlflow_provider

    def forecast_sales(self, forecast_request: ForecastRequest) -> ForecastResult:
        """Predicts the sales for a given item in a specific store on a specific date.

        Args:
            forecast_request: A ForecastRequest object containing the date, store, and item for which to predict sales.

        Returns:
            The forecasted sales.

        Raises:
            HTTPStatusError: If the request to the MLFlow inference server fails.
            ValidationError: If the response cannot be validated against the ForecastResult model.
        """

        # Feature engineering
        input_data = pd.DataFrame(
            [
                {
                    'store': forecast_request.store,
                    'item': forecast_request.item,
                    'month': forecast_request.date.month,
                    'day': forecast_request.date.weekday(),
                    'year': forecast_request.date.year,
                }
            ]
        )
        forecast_result = self.mlflow_provider.predict(input_data)
        return ForecastResult(predicted_sales=forecast_result.predictions[0])

    def health_check(self) -> bool:
        """Checks the health of the MLFlow inference server.

        Returns:
            True if the server is healthy, False otherwise.
        """
        return self.mlflow_provider.health_check()
