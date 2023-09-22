import requests


class UserService:
    url = "http://127.0.0.1:5000"
    create_user_endpoint = "/create"
    get_user_info_endpoint = "/user/info/"
    delete_user_endpoint = "/delete/"
    update_user_endpoint = "/update/"

    def __init__(self):
        pass

    def create_a_user(self, data):
        response = requests.post(self.url + self.create_user_endpoint, json=data)
        return response

    def get_user_info(self, user_id):
        response = requests.get(self.url + self.get_user_info_endpoint + str(user_id))
        return response

    def delete_a_user(self, user_id):
        response = requests.delete(self.url + self.delete_user_endpoint + str(user_id))
        return response

    def update_a_user(self, data, user_id):
        response = requests.put(self.url + self.update_user_endpoint + str(user_id), json=data)
        return response

    def check_service(self):
        response = requests.get(self.url)
        return response
