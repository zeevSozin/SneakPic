import requests

class modelBase:
    def __init__(self, endpointURI, base_route):
        self.endpointURI = endpointURI
        self.base_route = base_route
    def  get(self, route):
        res = requests.get(f"http://{self.endpointURI}/{self.base_route}/{route}")
        return res.json()

    def post(self, route, payload):
        url = f"http://{self.endpointURI}/{self.base_route}/{route}"
        res = requests.post(url, json = payload)
        return res



    def postFile(self, route, payload):
        url = f"http://{self.endpointURI}/{self.base_route}/{route}"
        res = requests.post(url, files = payload)
        return res
