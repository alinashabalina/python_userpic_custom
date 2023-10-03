import requests


class GroupService:
    url = "http://127.0.0.1:5001"
    create_group_endpoint = "/group/create"
    delete_group_endpoint = "/group/delete/"

    def __init__(self):
        pass

    def create_a_group(self, data):
        response = requests.post(self.url + self.create_group_endpoint, json=data)
        return response

    def delete_a_group(self, group_id, data):
        response = requests.delete(self.url + self.delete_group_endpoint + group_id)
        return response

    def check_service(self):
        response = requests.get(self.url)
        return response
