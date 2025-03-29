from typing import Any, List

from shared.data_model_base import ViewBase


class MLFlowResponse(ViewBase):
    """A class representing the response from an MLFlow inference server.

    Args:
        predictions: A list of predictions from the model.
    """

    predictions: List[Any]
