from provider.mlflow_provider import MLFlowProvider
from shared.dto.forecast_result import ForecastResult
from shared.view.request_view import ForecastRequest
import pandas as pd


class ForecastService:
    """A service for forecasting item sales.

    Args:
        met_provider: A client for an MLFlow Model which will produce the forecast.
    """

    def __init__(self, mlflow_provider: MLFlowProvider):
        self.mlflow_provider = mlflow_provider

    def forecast_sales(self, forecast_request: ForecastRequest) -> ForecastResult:
        """Searches the Metropolitan Museum of Art API by title.

        Args:
            forecast_request: A ForecastRequest object containing the title of the work to search for.

        Returns:
            The forecasted sales.

        Raises:
            HTTPStatusError: If the request to the MLFlow inference server fails.
            PydanticValidationError: If the response cannot be validated against the ForecastResult model.
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
