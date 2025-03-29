import os
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from provider.mlflow_provider import MLFlowProvider
from service.forecast_service import ForecastService
from shared.config.config_loader import load_config_settings
from shared.view.request_view import ForecastRequest
from shared.view.response_view import ForecastResponse
import httpx

app = FastAPI()
app_settings = load_config_settings(os.getenv('ENV', 'dev'))
forecast_service = ForecastService(MLFlowProvider(app_settings.model_api_url))


@app.post('/v1/api/predict')
def predict(request: ForecastRequest) -> ForecastResponse:
    """Predicts the sales for a given item in a specific store on a specific date.

    Args:
        request: A ForecastRequest object containing the date, store, and item for which to predict sales.

    Returns:
        A ForecastResponse object containing the predicted sales.
    """

    try:
        forecast_result = forecast_service.forecast_sales(request)
        return ForecastResponse(sales=forecast_result.predicted_sales)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.json())
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.get('/v1/api/health')
def health_check() -> dict:
    """Checks the health of the Service, including any dependencies.

    Returns:
        A dictionary indicating the health status of the server.
    """
    is_healthy = forecast_service.health_check()

    if is_healthy:
        return {'status': 'healthy'}
    else:
        raise HTTPException(status_code=503, detail='Service unavailable')
