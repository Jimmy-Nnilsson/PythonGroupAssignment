import requests
from datetime import datetime
import sqlite3
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
        result, score = self._format_text(self.r.text)
        self.out = {"date": str(datetime.now()),
                    "modeltype": self.modeltype,
                    "context": text,
                    "result": result,
                    "score": score}
        return self.out

    def _format_text(self, text):
        if "POSITIVE" in text:
            result = "POSITIVE"
        elif "NEGATIVE" in text:
            result = "NEGATIVE"

        score = text.split(":")[-1][:-1]
        score
        return result,score,


class MLQA(MLModel):
    def __init__(self, modeltype: str = "question_answering",
                       app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/question_answering/")
        super().__init__(modeltype=modeltype, app=app)

    def question_answering(self, question : str, context : str):
        context_question = {"context": context, "question": question}
        endpoint = (self.app + "/qa/")
        self.r = requests.post(url=endpoint, json=context_question)
        self.out = {"date": str(datetime.now()),
                    "modeltype": self.modeltype,
                    "context": context,
                    "result": self.r.text.split(":")[1][:-8],
                    "score": self.r.text.split(":")[-1][:-1],
                    "question": question}
        return self.out

class MLImageClassifier(MLModel):
    def __init__(self, modeltype: str = "image_classifier", app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/classify_image/")
        super().__init__(modeltype=modeltype, app=app)

    def _change_classes(self, new_classes:dict):
        r_class = requests.put(url=self.app + "/change_classes/", json=new_classes)
        pass

    def classify_image(self, file_path : str, classes : dict = {}):
        if classes != {}:
            self._change_classes(classes)
        files = {'file': open(file_path, 'rb')}
        self.r = requests.post(url=self.endpoint, files=files)
        self.out = {"date": str(datetime.now()),
                    "filename" : file_path.split("/")[-1],
                    "modeltype": self.modeltype,
                    "result": self.r.text,
                    "image": self._create_blob(file_path)}
        return self.out

    def _create_blob(self,filepath : str):
        # Convert digital data to binary format
        with open(filepath, 'rb') as file:
            blobData = file.read()
        return blobData

class databaseDB():
    def __init__(self, db_loc = 'data/dbgroup2.db') -> None:
        self.db_loc = db_loc
        self.db = sqlite3.Connection

    def createTables():
        pass

    def _connect(self):
        self.db = sqlite3.connect(self.db_loc)
        self.cursor = self.db.cursor()

    def insert(self, command : dict):
        self._connect()

        columns = [a for a in command.keys()]
        columns = ",".join(columns)
        values = [":" + a for a in command.keys()]
        values = ", ".join(values)
        execute = f'''INSERT INTO model({columns})
                    VALUES({values})'''
        self.cursor.execute(execute,
                            command)
        self.db.commit()
        self._disconnect()

    def _disconnect(self):
        self.db.close()

    def find_tables(self):
        self._connect()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        self._disconnect()
        return tables

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")