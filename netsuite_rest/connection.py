import json
import requests
import time
import oauth2 as oauth
from .SignSHA256 import SignatureMethod_HMAC_SHA256


class NS_Services:

    def __init__(self):
        self.CONSUMER_ID = "0bb156a24a337d8d2d6323d76dc655aa3e682839111e01f096ea6ded6e0f6ffa"
        self.CONSUMER_SECRET = "f06f8e9a8611eb9aa0ae1c5e7ed6b20ed742f25c9e33afa46eaab06bf38abfc9"
        self.TOKEN_ID = "c39621762979221db09e697c341be870d69cbf9dfb0b319668201429e833b487"
        self.TOKEN_SECRET = "ab6fbcedb4bc3ee2473aa273fafa9179b1139752516f8fe92c21e6d143398276"
        self.CONSUMER = oauth.Consumer(key=self.CONSUMER_ID, secret=self.CONSUMER_SECRET)
        self.TOKEN = oauth.Token(key=self.TOKEN_ID, secret=self.TOKEN_SECRET)
        self.ENDPOINT = f"https://7586908.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql?limit=1000"
        self.REALM = '7586908'

        self.CONSUMER_ID_SB = "9b6410f3cc08ffddde74606bcffe25f09744438d65588c1f1884368f0c6664ae"
        self.CONSUMER_SECRET_SB = "46555a11b49191e9f3af95405cdad0b931fa4861fd8a26a80403d42eb6ef72fa"
        self.TOKEN_ID_SB = "cb38dbeea1075a85610e2cb7f2191f396feda6065308695f1e4e4f2f0900d555"
        self.TOKEN_SECRET_SB = "ba20c9979714b030d98ba0b1fc92418e2c209828db2d1cb596b91b791d2b427d"
        self.CONSUMER_SB = oauth.Consumer(key=self.CONSUMER_ID_SB, secret=self.CONSUMER_SECRET_SB)
        self.TOKEN_SB = oauth.Token(key=self.TOKEN_ID_SB, secret=self.TOKEN_SECRET_SB)
        self.ENDPOINT_SB = f"https://7586908-sb1.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql?limit=1000"
        self.REALM_SB = '7586908_SB1'

    def get_results(self, ambiente: int, http_method: str, url_: str, data_raw_):

        consumer, token, token, url, realm, params = "", "", "", "", "", ""

        if ambiente == 1:
            consumer = self.CONSUMER
            token = self.TOKEN
            url = self.ENDPOINT
            realm = self.REALM
        elif ambiente == 2:
            consumer = self.CONSUMER_SB
            token = self.TOKEN_SB
            url = self.ENDPOINT_SB
            realm = self.REALM_SB
        if url_ == "":
            url_ = url
        if data_raw_ == "":
            data_raw_ = json.dumps({})

        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': str(int(time.time())),
            'oauth_token': token.key,
            'oauth_consumer_key': consumer.key
        }

        request = oauth.Request(method=http_method, url=url_, parameters=params)
        signature_method = SignatureMethod_HMAC_SHA256()
        request.sign_request(signature_method, consumer, token)
        header = request.to_header(realm)
        auth = header['Authorization'].encode('ascii', 'ignore')
        header = {'Authorization': auth, "Content-Type": "application/json", 'prefer': 'transient',
                  'Cookie': 'NS_ROUTING_VERSION=LAGGING', 'expandSubResources': 'true'}

        if http_method == 'POST' and url_.endswith("services/rest/record/v1/salesorder"):
            response = requests.request("POST", url_, headers=header, data=data_raw_)
            return response

        elif http_method == "POST":
            with requests.post(url=url_, headers=header, json=data_raw_) as connection:
                results = connection
            return results

        elif http_method == "DELETE":
            with requests.delete(url=url_, headers=header, json=data_raw_) as results:
                return results

        elif http_method == "GET":
            results = ""
            try:
                with requests.get(url=url_, headers=header, json=data_raw_) as connection:
                    results = connection
            except requests.exceptions.ConnectionError as e:
                results = f"Ocorreu um erro de conexão: {e}"
            except requests.exceptions.Timeout as e:
                results = f"A requisição excedeu o tempo limite: {e}"
            except requests.exceptions.RequestException as e:
                results = f"Ocorreu um erro na requisição: {e}"
            finally:
                return results

        elif http_method == "PATCH":
            response = requests.request("PATCH", url_, headers=header, json=data_raw_)
            results = response.text
            return results
