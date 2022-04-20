import os
import io
import time

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests


class ComputerVision:
    def __init__(self):
        self.API_key = '99ac96dad5b34b4683612fc2c6d8d67c'
        self.endpoint = 'https://cc-tema4.cognitiveservices.azure.com/'
        self.cv_client = self.init()

    def init(self):
        cv_client = ComputerVisionClient(self.endpoint, CognitiveServicesCredentials(self.API_key))

        return cv_client

    def identify_text_from_local_file(self, image_path):
        with open(image_path, 'rb') as image:
            response = self.cv_client.read_in_stream(
                image,
                Language='en',
                raw=True
            )

        operation_location = response.headers['Operation-Location']
        operation_id = operation_location.split('/')[-1]
        time.sleep(5)

        result = self.cv_client.get_read_result(operation_id)
        rr = result.analyze_result.read_results

        if result.status == OperationStatusCodes.succeeded:
            texts = ''
            for ar in rr:
                for line in ar.lines:
                    # print(line.text)
                    texts += line.text + '\n'
        else:
            texts = 'No hand write text found'

        return texts

    def identify_text_from_local_file_str(self, image_str):
        response = self.cv_client.read_in_stream(
                image_str,
                Language='en',
                raw=True
            )

        operation_location = response.headers['Operation-Location']
        operation_id = operation_location.split('/')[-1]
        time.sleep(5)

        result = self.cv_client.get_read_result(operation_id)
        rr = result.analyze_result.read_results

        if result.status == OperationStatusCodes.succeeded:
            texts = []
            for ar in rr:
                for line in ar.lines:
                    # print(line.text)
                    texts.append(line.text)
        else:
            texts = ['No hand write text found']

        return texts


# if __name__ == '__main__':
#     cv = ComputerVision()
#
#     r = cv.identify_text_from_local_file(r'C:\Users\Virgil\Desktop\CC Lab\Tema4-CC\computer_vision\hw.jpg')
#     print(r)