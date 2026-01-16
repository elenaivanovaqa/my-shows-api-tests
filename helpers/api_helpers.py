import requests


class ApiSession:
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def _send(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        result = self.session.request(method, self.base_url + endpoint, **kwargs)
        return result

    def get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        return self._send("GET", endpoint=endpoint, params=params)

    def post(self, endpoint: str, params: dict | None = None, body: dict | None = None) -> requests.Response:
        return self._send("POST", endpoint=endpoint, params=params, json=body)

    def put(self, endpoint: str, params: dict | None = None, body: dict | None = None) -> requests.Response:
        return self._send("PUT", endpoint=endpoint, params=params, json=body)

    def patch(self, endpoint: str, params: dict | None = None, body: dict | None = None) -> requests.Response:
        return self._send("PATCH", endpoint=endpoint, params=params, json=body)

    def delete(self, endpoint: str) -> requests.Response:
        return self._send("DELETE", endpoint=endpoint)
