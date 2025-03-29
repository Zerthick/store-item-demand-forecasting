import httpx
import pandas as pd

from shared.view.mlflow_view import MLFlowResponse


class MLFlowProvider:
    """A client an MLFlow inference server.

    Args:
        base_url: The base URL of the API.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def predict(self, input_data: pd.DataFrame) -> MLFlowResponse:
        """Sends a prediction request to the MLFlow inference server.

        Args:
            input_data: The input data for the prediction.

        Returns:
            The prediction response as a dictionary or None if the request fails.

        Raises:
            HTTPStatusError: If the request to the inference server fails.
            PydanticValidationError: If the response cannot be validated against the MLFlowResponse model.
        """

        payload = {'dataframe_split': input_data.to_dict(orient='split')}
        response = httpx.post(f'{self.base_url}/invocations', json=payload)
        response.raise_for_status()
        return MLFlowResponse.model_validate(response.json())

    def health_check(self) -> bool:
        """Checks the health of the MLFlow inference server.

        Returns:
            True if the server is healthy, False otherwise.
        """
        try:
            response = httpx.get(f'{self.base_url}/ping')
            return response.status_code == 200
        except httpx.RequestError:
            return False
