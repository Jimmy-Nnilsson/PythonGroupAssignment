import requests
from datetime import datetime
import subprocess
import sys

class MLModel():
    modelname = ["question_answering", "text_generator", "sentiment_analysis", "image_classifier"]

    def __init__(self, modeltype : str = "", app : str = "http://localhost:8000") -> None:
        self.app = app
        self.modeltype = modeltype
        self.r = requests.Response
        self.text = str
        self.p = subprocess.Popen
        self.out = {}

    def start(self):
        selected_model = {"name" : self.modeltype}
        endpoint= self.app + "/start/"
        self.r = requests.post(url=endpoint, json=selected_model)
        print(self.r.status_code)

    def run_server(self):
        sub_args=[sys.executable, 'src/main.py']
        self.p = subprocess.Popen(sub_args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, creationflags = subprocess.CREATE_NEW_CONSOLE,shell=True)

    def terminate_server(self):
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.p.pid))

    def st_stop_server(self,process):
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=process))

class MLTextGenerator(MLModel):
    def __init__(self, modeltype: str = "text_generator", app: str = "http://localhost:8000") -> None:
        super().__init__(modeltype=modeltype, app=app)

    def get_text_gen(self,text : str):
        context = {"context": text}
        endpoint = (self.app + "/text_generation/" )
        self.r = requests.post(url=endpoint, json=context)
        self._clean_text_gen()
        return{"date": str(datetime.now()),
        "modeltype": self.modeltype,
        "context": text,
        "result": self.r.text.split(":")[1][:-1]}

    def _clean_text_gen(self):
        modify = self.r.text[19:-2]
        newmodify = modify
        while '\\n' in newmodify or '  ' in newmodify:
            newmodify = newmodify.replace('\\n', ' ')
            newmodify = newmodify.replace('  ', ' ')
        self.text = newmodify


class MLSentimentAnalysis(MLModel):
    def __init__(self, modeltype: str = "sentiment_analysis", app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/sentiment_analysis/")
        super().__init__(modeltype=modeltype, app=app)

    def analyse_sentiment(self,text : str):
        context = {"context": text}
        endpoint = (self.app + "/sentiment_analysis/")
        self.r = requests.post(url=endpoint, json=context)
        result = dict(self.r.json())
        self.out = {"date": str(datetime.now()),
                    "modeltype": self.modeltype,
                    "context": text,
                    "result": result["sentiment_label"],
                    "score": result["score"]}
        return self.out
