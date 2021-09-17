import requests
from pathlib import Path
from PIL import Image
import os
from io import BytesIO

class MLModel():
    modelname = ["question_answering", "text_generator", "sentiment_analysis", "image_classifier"]

    def __init__(self, modeltype : str = "", app : str = "http://localhost:8000") -> None:
        self.app = app
        self.modeltype = modeltype
        self.r = requests.Response
        self.text = str

    def start(self):
        endpoint= self.app + "/start/items/" + self.modeltype
        self.modeltype = requests.get(url=endpoint)

class MLTextGenerator(MLModel):
    def __init__(self, modeltype: str = "text_generator", app: str = "http://localhost:8000") -> None:
        super().__init__(modeltype=modeltype, app=app)

    def get_text_gen(self,text : str):
        endpoint = (self.app + "/text_generation/items/" + text )
        self.r = requests.get(url=endpoint)
        self._clean_text_gen()

    def _clean_text_gen(self):
        modify = self.r.text[19:-2]
        newmodify = modify
        while '\\n' in newmodify or '  ' in newmodify:
            newmodify = newmodify.replace('\\n', ' ')
            newmodify = newmodify.replace('  ', ' ')
        self.text = newmodify

class MLImageClassifier(MLModel):
    def __init__(self, modeltype: str = "image_classifier", app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/classify_image/")
        super().__init__(modeltype=modeltype, app=app)

    def classify_image(self,file_path : str):
        files = {'file': open(file_path, 'rb')}
        self.r = requests.post(url=self.endpoint, files=files)
        print(self.r.text)

class MLSentimentAnalysis(MLModel):
    def __init__(self, modeltype: str = "sentiment_analysis", app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/sentiment_analysis/")
        super().__init__(modeltype=modeltype, app=app)

    def analyse_sentiment(self,text : str):
        endpoint = (self.app + "/sentiment_analysis/items/" + text )
        self.r = requests.get(url=endpoint)
        print(self.r.text)

class MLQA(MLModel):
    def __init__(self, modeltype: str = "question_answering", app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/question_answering/")
        super().__init__(modeltype=modeltype, app=app)

    def question_answering(self, question : str, context : str):
        endpoint = (self.app + "/qa/items/"+ question + "/" +context )
        self.r = requests.get(url=endpoint)
        print(self.r.text)