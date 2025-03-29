from shared.data_model_base import ViewBase
from datetime import datetime


class ForecastRequest(ViewBase):
    """A class representing a request to forecast item sales.

    Args:
        date: The date for which to forecast sales.
        store: The store ID for which to forecast sales.
        item: The item ID for which to forecast sales.
    """

    date: datetime
    store: int
    item: int
