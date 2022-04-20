import requests, uuid, json
from key_vault_secrets import get_secret

class Translate:

    def __init__(self):
        self.key = self.get_key()
        self.location = "northeurope"
        self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"

    def get_key(self):
        key = get_secret('translate-key')
        return key

    def translate(self, text):
        params = {
            'api-version': '3.0',
            'to': ['de']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': f"{text}"
        }]

        request = requests.post(self.endpoint, params=params, headers=headers, json=body)
        response = request.json()

        return response
