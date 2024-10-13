import json
import http.client
import requests

class Authentication:

    def __init__(self, api_key, client_id, client_secret):
        self.__api_key = api_key
        self.__client_id = client_id
        self.__client_secret = client_secret

    def request_token(self):
        try:
            url = 'https://airhub-api-dev.airspacelink.com/v1/oauth/token'
            headers = {
                'x-api-key': self.__api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.__client_id, 
                'client_secret': self.__client_secret, 
                'scope': 'route:create operation:create' 
            }

            response = requests.post(url, headers=headers, data=data)


            data = response.json() 
            token = data["data"]["accessToken"]
            return token

        except ValueError as ve:
            print("")
            print("ASL Authentication request error:")
            print("Value Error: %s", ve)
            print(response.text)
            print('HTTP Request failed')
            return response.text
        return None




# TESTING
def main():
    api_key = "f15b282e5bd6495eae4cafe2d42b72e5"
    client_id = "WxFWfnwgy0xieXdWws6OqMifV1nE9Ek6"
    client_secret = "IFTBdP00Ta4mrHZFgpjP-n4i-G0eVG-OL42IFnfvGaK4qO_bYGUPGhnwFaeVWXXZ"
    authentication = Authentication(api_key, client_id, client_secret)
    access_token = authentication.request_token()
    print(access_token)


if __name__ == '__main__':
    main()