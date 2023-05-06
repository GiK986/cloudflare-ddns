class CloudFlareConfig:
    def __init__(self, api_token, zone_id, record_name, ttl, proxy, check_interval):
        self.api_token = api_token
        self.zone_id = zone_id
        self.record_name = record_name
        self.ttl = ttl
        self.proxy = proxy
        self.check_interval = check_interval
        self.record_id = None

    @property
    def api_token(self):
        return self._api_token

    @api_token.setter
    def api_token(self, value):
        if not value:
            raise ValueError("CF_API_TOKEN is required")

        self._api_token = value

    @property
    def zone_id(self):
        return self._zone_id

    @zone_id.setter
    def zone_id(self, value):
        if not value:
            raise ValueError("CF_ZONE_ID is required")

        self._zone_id = value

    @property
    def record_name(self):
        return self._record_name

    @record_name.setter
    def record_name(self, value):
        if not value:
            raise ValueError("CF_RECORD_NAME is required")

        self._record_name = value

    @property
    def ttl(self):
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        if not value:
            value = 3600

        if value < 120:
            raise ValueError("ttl must be greater than 120")

        self._ttl = value

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        if not value:
            value = False

        self._proxy = value

    @property
    def check_interval(self):
        return self._check_interval

    @check_interval.setter
    def check_interval(self, value):
        if not value:
            value = 5

        if value < 1:
            raise ValueError("check_interval must be greater than 0")

        self._check_interval = value
