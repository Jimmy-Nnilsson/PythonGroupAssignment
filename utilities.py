import requests
import subprocess
import sys
import sqlite3
import streamlit as st
import pandas as pd

from datetime import datetime

class MLModel():
    """Machine learning superclass starts server and activates chosen ml model
    Methods: __init__
            start
            run_server
            st_stop_Server
    """
    def __init__(self, modeltype: str = "",
                 app: str = "http://localhost:8000") -> None:
        """Initializes class

        Args:
            modeltype (str, optional): choses what model to activate with
                                       the provided http command.
                                       Defaults to "".
            app (str, optional): Server on where the ml modelserver are located.
                                 Defaults to "http://localhost:8000".
        """
        self.app = app
        self.modeltype = modeltype
        self.r = requests.Response
        self.text = str
        self.p = subprocess.Popen
        self.out = {}

    def start(self):
        """Activates the selected modeltype on the machine learning server
        """
        selected_model = {"name": self.modeltype}
        endpoint = self.app + "/start/"
        try:
            self.r = requests.post(url=endpoint, json=selected_model)
            print(self.r.status_code, self.modeltype)
            if self.r.status_code == 200:
                return self.modeltype
            else:
                return ""
        except requests.exceptions.RequestException as e:
            print("No connection to ml server")
            return ""


    def run_server(self):
        """Runs the Machine learning server provided by nordaxon"""
        sub_args = [sys.executable, 'src/main.py']
        self.p = subprocess.Popen(sub_args,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  creationflags=subprocess.CREATE_NEW_CONSOLE,
                                  shell=True)

    def stop_server(self, process=""):
        """Stops the machine learning server provided by nordaxon

        Args:
            process (str, optional): What process number to kill.
                                     Defaults to "".
        """
        if process != "":
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=process))
        else:
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.p.pid))


class MLTextGenerator(MLModel):
    """Machine learning model textgenerator
    Methods: __init__
            start : from super class
            run_server : from super class
            st_stop_Server : from super class

            get_text_get
            _clean_text_gen
    """
    def __init__(self, modeltype: str = "text_generator",
                 app: str = "http://localhost:8000") -> None:
        """Intitializes class

        Args:
            modeltype (str, optional): modeltype to use for commands.
                                       Defaults to "text_generator".
            app (str, optional): Machine learning server adress.
                                 Defaults to "http://localhost:8000".
        """
        super().__init__(modeltype=modeltype, app=app)

    def get_text_gen(self, text: str) -> dict:
        """Machine learning model generates text on provided string

        Args:
            text (str): Start text for the machine learning model

        Returns:
            dict: outputs date, modeltype, contex and result in a dictionary
        """
        context = {"context": text}
        endpoint = (self.app + "/text_generation/")
        self.out = {"date": str(datetime.now()),
                    "modeltype": self.modeltype,
                    "context": text,
                    "result": "ConnectionError"}
        try:
            self.r = requests.post(url=endpoint, json=context)
            self._clean_text_gen()
            #self.out["result"] = self.r.text.split(":")[1][:-1]
            self.out["result"] = self.r.text

        except requests.exceptions.RequestException as e:
            print("No connection to ml server")
        return self.out

    def _clean_text_gen(self):

        """Cleans api result from linebreaks and double spaces
        """
        modify = self.r.text.strip()
        newmodify = modify
        print("garbage cleaner!!!!")
        self.text = newmodify


class MLSentimentAnalysis(MLModel):
    """Machine learning model textgenerator
    Methods: __init__
            start : from super class
            run_server : from super class
            st_stop_Server : from super class

            analyes_sentiment
    """
    def __init__(self, modeltype: str = "sentiment_analysis",
                 app: str = "http://localhost:8000") -> None:
        """Intitializes class

        Args:
            modeltype (str, optional): modeltype to use for commands.
                                       Defaults to "text_generator".
            app (str, optional): Machine learning server adress.
                                 Defaults to "http://localhost:8000".
        """
        self.endpoint = (app + "/sentiment_analysis/")
        super().__init__(modeltype=modeltype, app=app)

    def analyse_sentiment(self, text: str) -> dict:
        """Machine learning model generates analyses sentiment on
           provided string

        Args:
            text (str): Text to analyse

        Returns:
            dict: outputs date, modeltype, contex and result in a dictionary
        """
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
    """Machine learning model image classifier
    Methods: __init__
            start : from super class
            run_server : from super class
            st_stop_Server : from super class

            _change_classes
            classify_image
    """
    def __init__(self, modeltype: str = "image_classifier",
                 app: str = "http://localhost:8000") -> None:
        """Intitializes class

        Args:
            modeltype (str, optional): modeltype to use for commands.
                                       Defaults to "text_generator"
            app (str, optional): Machine learning server adress.
                                 Defaults to "http://localhost:8000"
        """
        self.endpoint = (app + "/classify_image/")
        super().__init__(modeltype=modeltype, app=app)

    def _change_classes(self, new_classes: dict):
        """Changes the class used to try to match the picture to

        Args:
            new_classes (dict): new classes in the format
            {"class_1 : "", "class_2" : "", "class_3" : ""}
        """
        r_class = requests.put(url=self.app + "/change_classes/",
                               json=new_classes)

    def classify_image(self,
                       file: bytes,
                       classes: dict = {},
                       name: str = "") -> dict:
        """Classifies image to provided or default classes.

        Args:
            file (bytes): imagefile to classify
            classes (dict, optional): Classes to compare to. Defaults to {}.
            name (str, optional): filename. Defaults to "".

        Returns:
            dict: date, modeltype, result, image in a dictionary
        """
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


class MLQA(MLModel):
    """Machine learning model question answering
    Methods: __init__
            start : from super class
            run_server : from super class
            st_stop_Server : from super class

            question_answering
    """
    def __init__(self, modeltype: str = "question_answering",
                 app: str = "http://localhost:8000") -> None:
        """Intitializes class

        Args:
            modeltype (str, optional): modeltype to use for commands.
                                       Defaults to "text_generator".
            app (str, optional): Machine learning server adress.
                                 Defaults to "http://localhost:8000".
        """
        super().__
        self.endpoint = (app + "/question_answering/")
        super().__init__(modeltype=modeltype, app=app)

    def question_answering(self, question: str, context: str) -> dict:
        """Machine learning model generates answeres on provided text
           and question

        Args:
            question (str): Question to find answer on
            context (str): Source to find answer on

        Returns:
            dict: outputs date,
                          modeltype,
                          contex,
                          result,
                          score and question in a dictionary
        """
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


def _text_generator_to_db(cursor: sqlite3.Cursor,
                          database_connection: sqlite3.Connection,
                          input: dict):
    text_generator_table_create_command = """CREATE TABLE IF NOT EXISTS text_generator(
                                             id INTEGER PRIMARY KEY,
                                             date TEXT NOT NULL,
                                             context TEXT NOT NULL,
                                             result TEXT NOT NULL)"""
    text_generator_insert_query = """INSERT INTO text_generator
                                    (date, context, result) VALUES (?, ?, ?)"""

    cursor.execute(text_generator_table_create_command)
    # text_generator data tuple values [date, context, result]
    data_tuple = (input["date"], input["context"], input["result"])
    cursor.execute(text_generator_insert_query, data_tuple)
    database_connection.commit()
    cursor.close()


def _image_classifier_to_db(cursor: sqlite3.Cursor,
                            database_connection: sqlite3.Connection,
                            input: dict):
    image_classifier_table_create_command = """CREATE TABLE IF NOT EXISTS image_classifier(
                                               id INTEGER PRIMARY KEY,
                                               date TEXT NOT NULL,
                                               filename TEXT NOT NULL,
                                               result TEXT NOT NULL,
                                               image BLOB NOT NULL)"""
    image_classifier_insert_query = """INSERT INTO image_classifier
                                    (date, filename, result, image) VALUES (?, ?, ?, ?)"""
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


def _sentiment_analysis_to_db(cursor: sqlite3.Cursor,
                              database_connection: sqlite3.Connection,
                              input: dict):
    sentiment_analysis_table_create_command = """CREATE TABLE IF NOT EXISTS sentiment_analysis(
                                                 id INTEGER PRIMARY KEY,
                                                 date TEXT NOT NULL,
                                                 context TEXT NOT NULL,
                                                 result TEXT NOT NULL,
                                                 score TEXT NOT NULL)"""
    sentiment_analysis_insert_query = """INSERT INTO sentiment_analysis
                                    (date, context, result, score) VALUES (?, ?, ?, ?)"""
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


def _question_answering_to_db(cursor: sqlite3.Cursor,
                              database_connection: sqlite3.Connection,
                              input: dict):

    question_answering_table_create_command = """CREATE TABLE IF NOT EXISTS question_answering(
                                                 id INTEGER PRIMARY KEY,
                                                 date TEXT NOT NULL,
                                                 context TEXT NOT NULL,
                                                 result TEXT NOT NULL,
                                                 score TEXT NOT NULL,
                                                 question TEXT NOT NULL)"""
    question_answering_insert_query = """INSERT INTO question_answering
                                    (date, context, result, score, question) VALUES (?, ?, ?, ?, ?)"""

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


def write_to_db(input: dict):

    default_db_name = "main_database.db"
    data_tuple = None
    print(input['modeltype'])

    try:
        database_connection = sqlite3.connect(default_db_name)
        cursor = database_connection.cursor()
        print("Connected to SQLite")

        if(input['modeltype'] == "text_generator"):
            _text_generator_to_db(cursor, database_connection, input)

        elif(input['modeltype'] == "sentiment_analysis"):
            _sentiment_analysis_to_db(cursor, database_connection, input)

        elif(input['modeltype'] == "image_classifier"):
            _image_classifier_to_db(cursor, database_connection, input)

        elif(input['modeltype'] == "question_answering"):
            _question_answering_to_db(cursor, database_connection, input)

        else:
            print("Error! Not a valid model type.")

    except sqlite3.Error as error:
        print("Failed to insert data into SQLite database", error)

    finally:
        if database_connection:
            database_connection.close()
            print("SQLite connection is closed")

			
			
def view_db_log(model:str):
    default_db_name = "main_database.db"
    db = sqlite3.connect(default_db_name)
    df = None
    try:
        if(model == "text_generator"):
            df = pd.read_sql("SELECT * FROM text_generator", db)

        elif(model == "sentiment_analysis"):
            df = pd.read_sql("SELECT * FROM sentiment_analysis", db)

        elif(model == "image_classifier"):
            df = pd.read_sql("SELECT * FROM image_classifier", db)

        elif(model == "question_answering"):
            df = pd.read_sql("SELECT * FROM question_answering", db)
        else:
            print("Error! Not a valid model type.")
    except pd.io.sql.DatabaseError as error:
        print("Database was not found!", error)
    finally:
        db.close()
        st.write(df)