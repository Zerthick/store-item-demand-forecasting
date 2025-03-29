import pytest
from unittest.mock import MagicMock
from service.forecast_service import ForecastService
from provider.mlflow_provider import MLFlowProvider
from shared.view.mlflow_view import MLFlowResponse
from shared.view.request_view import ForecastRequest
from datetime import datetime


@pytest.fixture
def mock_mlflow_provider() -> MLFlowProvider:
    """Fixture to mock the MLFlowProvider."""
    mlflow_provider = MagicMock()

    mock_predict_reponse = MLFlowResponse(predictions=[12.3])
    mlflow_provider.predict.return_value = mock_predict_reponse

    mock_health_response = True
    mlflow_provider.health_check.return_value = mock_health_response

    return mlflow_provider


def test_forecast_service_predict(mock_mlflow_provider):
    # GIVEN
    forecast_service = ForecastService(mock_mlflow_provider)
    forecast_request = ForecastRequest(date=datetime(year=2013, month=1, day=1), store=1, item=1)

    # WHEN
    result = forecast_service.forecast_sales(forecast_request)

    # THEN
    assert result.predicted_sales == 12.3
    mock_mlflow_provider.predict.assert_called_once()


def test_forecast_service_health_check(mock_mlflow_provider):
    # GIVEN
    forecast_service = ForecastService(mock_mlflow_provider)

    # WHEN
    result = forecast_service.health_check()

    # THEN
    assert result is True
    mock_mlflow_provider.health_check.assert_called_once()
