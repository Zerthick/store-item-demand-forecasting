from shared.data_model_base import ViewBase


class ForecastResponse(ViewBase):
    """A class representing a response to forecast item sales.

    Args:
        sales: The forecasted sales value.
    """

    sales: float
