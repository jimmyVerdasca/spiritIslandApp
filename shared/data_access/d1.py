from .base import DataProvider

class D1DataProvider(DataProvider):
    
    def __init__(
        self,
        account_id,
        api_token,
        database_id,
    ):
        self.account_id = account_id
        self.api_token = api_token
        self.database_id = database_id