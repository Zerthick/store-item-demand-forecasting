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
    """Executes a search against the Metropolitan Museum of Art API and returns the url of the primary image of the first search result.

    Args:
        title: The title of the work you wish to search for.

    Returns:
        The url of the primary image of the first search result or 'No results found.' if no search results are found.
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
        raise HTTPException(status_code=503, detail='Service Unavailable')
