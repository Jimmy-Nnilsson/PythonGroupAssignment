import requests
from datetime import datetime
import subprocess
import sys
import sqlite3

class MLModel():
    modelname = ["question_answering",
                 "text_generator",
                 "sentiment_analysis",
                 "image_classifier"]

    def __init__(self, modeltype : str = "", 
                 app : str = "http://localhost:8000") -> None:
        self.app = app
        self.modeltype = modeltype
        self.r = requests.Response
        self.text = str
        self.p = subprocess.Popen
        self.out = {}

    def start(self):
        selected_model = {"name": self.modeltype}
        endpoint = self.app + "/start/"
        try:
            self.r = requests.post(url=endpoint, json=selected_model)
            print(self.r.status_code, self.modeltype)
        except requests.exceptions.RequestException as e:
            print("No connection to ml server")


    def run_server(self):
        sub_args = [sys.executable, 'src/main.py']
        self.p = subprocess.Popen(sub_args,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  creationflags=subprocess.CREATE_NEW_CONSOLE,
                                  shell=True)

    def terminate_server(self):
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.p.pid))

    def st_stop_server(self, process):
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=process))


class MLTextGenerator(MLModel):
    def __init__(self, modeltype: str = "text_generator",
                 app: str = "http://localhost:8000") -> None:
        super().__init__(modeltype=modeltype, app=app)

    def get_text_gen(self, text: str):
        context = {"context": text}
        endpoint = (self.app + "/text_generation/")
        self.out = {"date": str(datetime.now()),
                "modeltype": self.modeltype,
                "context": text,
                "result": "ConnectionError"}
        try:
            self.r = requests.post(url=endpoint, json=context)
            self._clean_text_gen()
            self.out["result"] = self.r.text.split(":")[1][:-1]

        except requests.exceptions.RequestException as e:
            print("No connection to ml server")
        return self.out

    def _clean_text_gen(self):
        modify = self.r.text[19:-2]
        newmodify = modify
        while '\\n' in newmodify or '  ' in newmodify:
            newmodify = newmodify.replace('\\n', ' ')
            newmodify = newmodify.replace('  ', ' ')
        self.text = newmodify


class MLSentimentAnalysis(MLModel):
    def __init__(self, modeltype: str = "sentiment_analysis",
                 app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/sentiment_analysis/")
        super().__init__(modeltype=modeltype, app=app)

    def analyse_sentiment(self, text: str):
        context = {"context": text}
        endpoint = (self.app + "/sentiment_analysis/")
        self.out = {"date": str(datetime.now()),
                    "modeltype": self.modeltype,
                    "context": text,
                    "result": "ConnectionError",
                    "score": ""}
        try:
            self.r = requests.post(url=endpoint, json=context)
            result = dict(self.r.json())
            self.out["result"] = result["sentiment_label"]
            self.out["score"] = result["score"]
        except requests.exceptions.RequestException as e:
            print("No connection to ml server")

        return self.out


class MLImageClassifier(MLModel):
    def __init__(self, modeltype: str = "image_classifier",
                 app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/classify_image/")
        super().__init__(modeltype=modeltype, app=app)

    def _change_classes(self, new_classes: dict):
        r_class = requests.put(url=self.app + "/change_classes/",
                               json=new_classes)

    def classify_image(self, file, classes: dict = {}, name=""):
        if classes != {}:
            self._change_classes(classes)
        files = {'file': file}
        self.out = {"date": str(datetime.now()),
                        "filename": name,
                        "modeltype": self.modeltype,
                        "result": "ConnectionError",
                        "image": file}
        try:
            self.r = requests.post(url=self.endpoint, files=files)
            self.out["result"] = self.r.text
        except requests.exceptions.RequestException as e:
            print("No connection to ml server")

        return self.out

    def _create_blob(self, filepath: str):
        # Convert digital data to binary format
        with open(filepath, 'rb') as file:
            blobData = file.read()
        return blobData


class MLQA(MLModel):
    def __init__(self, modeltype: str = "question_answering",
                 app: str = "http://localhost:8000") -> None:
        self.endpoint = (app + "/question_answering/")
        super().__init__(modeltype=modeltype, app=app)

    def question_answering(self, question: str, context: str):
        context_question = {"context": context, "question": question}
        endpoint = (self.app + "/qa/")

        self.out = {"date": str(datetime.now()),
                    "modeltype": self.modeltype,
                    "context": context,
                    "result": "ConnectionError",
                    "score": "",
                    "question": question}
        try:
            self.r = requests.post(url=endpoint, json=context_question)
            self.out["result"] = self.r.text.split(":")[1][:-8]
            self.out["score"] = self.r.text.split(":")[-1][:-1]
        except requests.exceptions.RequestException as e:
            print("No connection to ml server")
        return self.out


def write_to_db(input: dict):

    default_db_name = "main_database.db"

    text_generator_table_create_command = """CREATE TABLE IF NOT EXISTS text_generator(
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    context TEXT NOT NULL,
    result TEXT NOT NULL)
"""

    sentiment_analysis_table_create_command = """CREATE TABLE IF NOT EXISTS sentiment_analysis(
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    context TEXT NOT NULL,
    result TEXT NOT NULL,
    score TEXT NOT NULL)
"""

    image_classifier_table_create_command = """CREATE TABLE IF NOT EXISTS image_classifier(
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    filename TEXT NOT NULL,
    result TEXT NOT NULL,
    image BLOB NOT NULL)
"""

    question_answering_table_create_command = """CREATE TABLE IF NOT EXISTS question_answering(
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    context TEXT NOT NULL,
    result TEXT NOT NULL,
    score TEXT NOT NULL,
    question TEXT NOT NULL)
"""

    text_generator_insert_query = """INSERT INTO text_generator
                                    (date, context, result) VALUES (?, ?, ?)"""
    sentiment_analysis_insert_query = """INSERT INTO sentiment_analysis
                                    (date, context, result, score) VALUES (?, ?, ?, ?)"""
    image_classifier_insert_query = """INSERT INTO image_classifier
                                    (date, filename, result, image) VALUES (?, ?, ?, ?)"""
    question_answering_insert_query = """INSERT INTO question_answering
                                    (date, context, result, score, question) VALUES (?, ?, ?, ?, ?)"""

    data_tuple = None
    print(input['modeltype'])
    try:
        database_connection = sqlite3.connect(default_db_name)
        cursor = database_connection.cursor()
        print("Connected to SQLite")

        if(input['modeltype'] == "text_generator"):
            cursor.execute(text_generator_table_create_command)
            # text_generator data tuple values [date, context, result]
            data_tuple = (input["date"], input["context"], input["result"])
            cursor.execute(text_generator_insert_query, data_tuple)
            database_connection.commit()
            cursor.close()

        elif(input['modeltype'] == "sentiment_analysis"):
            cursor.execute(sentiment_analysis_table_create_command)
            # sentiment_analysis data tuple values
            # [date, context, result, score]
            data_tuple = (input["date"],
                          input["context"],
                          input["result"],
                          input["score"])
            cursor.execute(sentiment_analysis_insert_query, data_tuple)
            database_connection.commit()
            cursor.close()

        elif(input['modeltype'] == "image_classifier"):
            cursor.execute(image_classifier_table_create_command)
            # image_classifier data tuple values
            # [date, filename, result, image]
            data_tuple = (input["date"],
                          input["filename"],
                          input["result"],
                          input["image"])
            cursor.execute(image_classifier_insert_query, data_tuple)
            database_connection.commit()
            cursor.close()

        elif(input['modeltype'] == "question_answering"):
            cursor.execute(question_answering_table_create_command)
            # question_answering data tuple values
            # [date, context, result, score, question]
            data_tuple = (input["date"],
                          input["context"],
                          input["result"],
                          input["score"],
                          input["question"])
            cursor.execute(question_answering_insert_query, data_tuple)
            database_connection.commit()
            cursor.close()

        else:
            print("Error! Not a valid model type.")

    except sqlite3.Error as error:
        print("Failed to insert data into SQLite database", error)

    finally:
        if database_connection:
            database_connection.close()
            print("SQLite connection is closed")
