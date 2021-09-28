"""Help classes and functions for group2 streamlit ml app
"""
import sys
import subprocess
import sqlite3
import json
from datetime import datetime
import requests
import streamlit as st
import pandas as pd


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
        self.response = requests.Response
        self.text = str
        self.serverprocess = subprocess.Popen
        self.out = {}

    def start(self):
        """Activates the selected modeltype on the machine learning server
        """
        selected_model = {"name": self.modeltype}
        endpoint = self.app + "/start/"
        try:
            self.response= requests.post(url=endpoint, json=selected_model)
            print(self.response.status_code, self.modeltype)
            if self.response.status_code == 200:
                active_model = self.modeltype
            else:
                active_model = "Error"
        except requests.exceptions.RequestException as error_type:
            print("No connection to ml server", error_type)
            active_model = "Error"
        return active_model


    def run_server(self):
        """Runs the Machine learning server provided by nordaxon"""
        sub_args = [sys.executable, 'src/main.py']
        self.serverprocess = subprocess.Popen(sub_args,
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
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.serverprocess.pid))


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
            self.response= requests.post(url=endpoint, json=context)
            self._clean_text_gen()
            #self.out["result"] = self.response.text.split(":")[1][:-1]
            self.out["result"] = self.response.text

        except requests.exceptions.RequestException as error_type:
            print("No connection to ml server", error_type)
        return self.out

    def _clean_text_gen(self):

        """Cleans api result from linebreaks and double spaces
        """
        modify = self.response.text.strip()
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
            self.response= requests.post(url=endpoint, json=context)
            result = dict(self.response.json())
            self.out["result"] = result["sentiment_label"]
            self.out["score"] = result["score"]
        except requests.exceptions.RequestException as errortype:
            print("No connection to ml server", errortype)

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
        requests.put(url=self.app + "/change_classes/",
                     json=new_classes)

    def classify_image(self,
                       file: bytes,
                       classes: dict = None,
                       name: str = "") -> dict:
        """Classifies image to provided or default classes.

        Args:
            file (bytes): imagefile to classify
            classes (dict, optional): Classes to compare to. Defaults to {}.
            name (str, optional): filename. Defaults to "".

        Returns:
            dict: date, modeltype, result, image in a dictionary
        """
        if classes is not None:
            self._change_classes(classes)
        files = {'file': file}
        self.out = {"date": str(datetime.now()),
                    "filename": name,
                    "modeltype": self.modeltype,
                    "result": "ConnectionError",
                    "image": file}
        try:
            self.response= requests.post(url=self.endpoint, files=files)
            self.out["result"] = self.response.text
        except requests.exceptions.RequestException as errortype:
            print("No connection to ml server", errortype)
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
            self.response= requests.post(url=endpoint, json=context_question)
            self.out["result"] = self.response.text.split(":")[1][:-8]
            self.out["score"] = self.response.text.split(":")[-1][:-1]
        except requests.exceptions.RequestException as errortype:
            print("No connection to ml server", errortype)
        return self.out


def _text_generator_to_db(cursor: sqlite3.Cursor,
                          database_connection: sqlite3.Connection,
                          user_input: dict):
    text_generator_table_create_command = """CREATE TABLE IF NOT EXISTS text_generator(
                                             id INTEGER PRIMARY KEY,
                                             date TEXT NOT NULL,
                                             context TEXT NOT NULL,
                                             result TEXT NOT NULL)"""
    text_generator_insert_query = """INSERT INTO text_generator
                                    (date, context, result) VALUES (?, ?, ?)"""

    cursor.execute(text_generator_table_create_command)
    # text_generator data tuple values [date, context, result]
    data_tuple = (user_input["date"], user_input["context"], user_input["result"])
    cursor.execute(text_generator_insert_query, data_tuple)
    database_connection.commit()
    cursor.close()


def _image_classifier_to_db(cursor: sqlite3.Cursor,
                            database_connection: sqlite3.Connection,
                            user_input: dict):
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
    data_tuple = (user_input["date"],
                  user_input["filename"],
                  user_input["result"],
                  user_input["image"])
    cursor.execute(image_classifier_insert_query, data_tuple)
    database_connection.commit()
    cursor.close()


def _sentiment_analysis_to_db(cursor: sqlite3.Cursor,
                              database_connection: sqlite3.Connection,
                              user_input: dict):
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
    data_tuple = (user_input["date"],
                  user_input["context"],
                  user_input["result"],
                  user_input["score"])
    cursor.execute(sentiment_analysis_insert_query, data_tuple)
    database_connection.commit()
    cursor.close()


def _question_answering_to_db(cursor: sqlite3.Cursor,
                              database_connection: sqlite3.Connection,
                              user_input: dict):

    question_answering_table_create_command = """CREATE TABLE IF NOT EXISTS question_answering(
                                                 id INTEGER PRIMARY KEY,
                                                 date TEXT NOT NULL,
                                                 context TEXT NOT NULL,
                                                 result TEXT NOT NULL,
                                                 score TEXT NOT NULL,
                                                 question TEXT NOT NULL)"""
    question_answering_insert_query = """INSERT INTO question_answering
                                      (date,
                                       context,
                                       result,
                                       score,
                                       question) VALUES (?, ?, ?, ?, ?)"""

    cursor.execute(question_answering_table_create_command)
    # question_answering data tuple values
    # [date, context, result, score, question]
    data_tuple = (user_input["date"],
                  user_input["context"],
                  user_input["result"],
                  user_input["score"],
                  user_input["question"])
    cursor.execute(question_answering_insert_query, data_tuple)
    database_connection.commit()
    cursor.close()


def write_to_db(user_input: dict):
    """Writes information to the sql database

    Args:
        user_input (dict): Output from the machine learning classes
    """
    default_db_name = "main_database.db"
    print(user_input['modeltype'])

    try:
        database_connection = sqlite3.connect(default_db_name)
        cursor = database_connection.cursor()
        print("Connected to SQLite")

        if user_input['modeltype'] == "text_generator":
            _text_generator_to_db(cursor, database_connection, user_input)

        elif user_input['modeltype'] == "sentiment_analysis":
            _sentiment_analysis_to_db(cursor, database_connection, user_input)

        elif user_input['modeltype'] == "image_classifier":
            _image_classifier_to_db(cursor, database_connection, user_input)

        elif user_input['modeltype'] == "question_answering":
            _question_answering_to_db(cursor, database_connection, user_input)

        else:
            print("Error! Not a valid model type.")

    except sqlite3.Error as error:
        print("Failed to insert data into SQLite database", error)

    finally:
        if database_connection:
            database_connection.close()
            print("SQLite connection is closed")


def view_db_log(model: str):
    """Creates view of current model table from the sql database

    Args:
        model (str): chosses model to view
    """
    default_db_name = "main_database.db"
    database = sqlite3.connect(default_db_name)
    try:
        if model == "text_generator":
            df_database = pd.read_sql("SELECT * FROM text_generator", database)

        elif model == "sentiment_analysis":
            df_database = pd.read_sql("SELECT * FROM sentiment_analysis", database)

        elif model == "image_classifier":
            df_database = pd.read_sql("SELECT * FROM image_classifier", database)

        elif model == "question_answering" :
            df_database = pd.read_sql("SELECT * FROM question_answering", database)
        else:
            print("Error! Not a valid model type.")
    except pd.io.sql.DatabaseError as error:
        print("Database was not found!", error)
    finally:
        database.close()
        st.write(df_database)


def get_id_db_log(columns: str, rowid: str, model: str) -> list:
    """Get an isolated row with selected columns from the model
       table

    Args:
        columns (str): Columns to choose from the table
        rowid (str): Rownumber to output from the table
        model (str): what table to access

    Returns:
        list: the row with selected columns
    """
    default_db_name = "main_database.db"
    database = sqlite3.connect(default_db_name)
    cur = database.cursor()

    cur.execute(f'''SELECT {columns} FROM {model} WHERE id =='{rowid}' ''')
    df_database = cur.fetchall()

    database.close()
    return df_database


def body_sidebar() -> str:
    """Streamlit page for the sidebar
    starts Machine learning server.
    Chooses what machine learning model to use.

    Returns:
        str: selected_ml_model what model is chosen in the selector
    """
    if 'running_model' not in st.session_state:
        st.session_state['running_model'] = ""
    if 'server_pid' not in st.session_state:
        st.session_state['server_pid'] = 0
    ml_server = MLModel()

    btn_start_ml = st.sidebar.button("Start ML Model Server")
    btn_stop_ml = st.sidebar.button("Stop ML Model Server")

    if btn_start_ml:
        if st.session_state['server_pid'] == 0:
            ml_server.run_server()
            st.session_state['server_pid'] = ml_server.serverprocess.pid
    if btn_stop_ml:
        if st.session_state['server_pid'] != 0:
            ml_server.stop_server(st.session_state['server_pid'])
            st.session_state['server_pid'] = 0

    st.sidebar.write(f"PID {str(st.session_state['server_pid'])}")
    selected_ml_model = st.sidebar.selectbox("Select ML Model",
                                            ["question_answering",
                                            "text_generator",
                                            "sentiment_analysis",
                                            "image_classifier"])
    return selected_ml_model


def body_image_class():
    """Streamlit page function for changing imageclasses
       for image classifier
    """
    with st.expander("Image classes"):
        with st.form("ML Classes"):
            image_class1 = st.text_input("Image Class 1: ")
            image_class2 = st.text_input("Image Class 2: ")
            image_class3 = st.text_input("Image Class 3: ")
            submit_classes = st.form_submit_button("Submit Classes")
    if submit_classes:
        st.session_state["image_classes"] = {"class_1": image_class1,
                                             "class_2": image_class2,
                                             "class_3": image_class3}

def body_image_classifier():
    """Streamlit page for image classifier
       tries to classify a picture between 3 different
       classes. Either default or provided by user.
       also acesses database for using historical queries
    """
    image_classifier = MLImageClassifier()
    if 'image_classes' not in st.session_state:
        st.session_state['image_classes'] = {}

    if st.session_state['running_model'] != "image_classifier":
        st.session_state['running_model'] = image_classifier.start()

    col1, col2 = st.columns([10, 10])
    with col1:
        st.header("Image Classifier")

        body_image_class()
        upload = st.file_uploader("Image", type=[".jpg", ".jpeg", '.png'])
        btn_classify = st.button("Classify Image")
        container = st.container()

    with st.form("Forms with things"):
        btn_update_log = st.form_submit_button("Update Log")
        regenerate_id = st.text_input("Input Id to classify")
        col3, col4 = st.columns(2)
        with col3:
            btn_classify_table = st.form_submit_button("Classify Table Id")
        with col4:
            btn_show_id = st.form_submit_button("Show Old result")

    if btn_update_log:
        view_db_log("image_classifier")

    if btn_classify_table or btn_show_id:
        file = get_id_db_log("image,filename,result",
                                regenerate_id,
                                "image_classifier")
        if file != []:
            upload = file[0][0]
        else:
            st.write("Database index out of range")

    with container:
        if (btn_classify or btn_classify_table or btn_show_id) and upload is not None:
            if btn_classify:
                file = upload.getvalue()
                out = image_classifier.classify_image(file,
                                                        st.session_state["image_classes"],
                                                        upload.name)
                write_to_db(out)
                result_dict = dict(image_classifier.response.json())
            elif btn_classify_table:
                out = image_classifier.classify_image(upload,
                                                        st.session_state["image_classes"],
                                                        file[0][1])
                write_to_db(out)
                result_dict = dict(image_classifier.response.json())
            elif btn_show_id:
                result_dict = json.loads(file[0][2].replace("'", "\""))
            best_match = sorted(result_dict, key=result_dict.get, reverse=True)[0]
            st.text(f"From the classes the best match is: {best_match.capitalize()}")
            st.text(f"with a probability of {round(float(result_dict[best_match])*100,1)}%")
            classes_string = str(result_dict.keys())
            st.text(f"From the classes: {classes_string[12:-2]}")
    with col2:
        if upload is not None:
            st.image(upload)

def body_text_generator():
    """Streamlit page for text generator
       takes a text and tries to continue on it
       also acesses database for using historical queries
    """
    text_generator = MLTextGenerator()
    st.header("text generator")
    if st.session_state['running_model'] != "text_generator":
        st.session_state['running_model'] = text_generator.start()

    st.write("Here you can add any word or sentence and get it generated further")
    trash = st.empty()
    col1, col3 = st.columns(2)

    with col1:
        user_input = st.text_input("")
        text_generator_button = st.button("Generate")
    my_expander = st.expander(label="Show logs", expanded=False)

    with my_expander:
        database = sqlite3.connect("main_database.db")
        database.commit()
        df_database = pd.read_sql("SELECT * FROM text_generator", database)
        df_database = df_database.set_index("id")
        database.close()
        st.dataframe(df_database)
        update_log_button = st.button("Update")

    if update_log_button:
        database = sqlite3.connect("main_database.db")
        database.commit()
        df_database = pd.read_sql("SELECT * FROM text_generator", database)
        df_database = df_database.set_index("id")
        database.close()

    if text_generator_button:
        user_result = text_generator.get_text_gen(user_input)
        write_to_db(user_result)
        text_generator.response.json()
        duser_result = dict(text_generator.response.json())
        st.success('Sucessfully generated text')
        st.write(duser_result["generated_text"])


def body_sentiment_analysis():
    """Streamlit page for sentiment analysis
       takes a string and analyses its sentiment
       also acesses database for using historical queries
    """
    sentiment_analysis = MLSentimentAnalysis()
    st.header("Sentiment analysis")
    if st.session_state['running_model'] != "sentiment_analysis":
        st.session_state['running_model'] = sentiment_analysis.start()
    with st.form(key='Get data'):
        user_input = st.text_input(label='Enter text you want to analyse')
        submit_button_2 = st.form_submit_button(label='Submit')
    if submit_button_2:
        user_result = sentiment_analysis.analyse_sentiment(str(user_input))
        st.write(str(round(user_result["score"] * 100, 1)) + "%", user_result["result"])
        write_to_db(user_result)
    if st.button("Click here to view data"):
        view_db_log("sentiment_analysis")
    with st.form(key='Get data by ID'):
        user_id_input = st.text_input(label='Enter ID')
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        sql_list = get_id_db_log("context", user_id_input, "sentiment_analysis")
        user_result = sentiment_analysis.analyse_sentiment(str(sql_list[0]))
        st.write(str(round(user_result["score"] * 100, 1)) + "%", user_result["result"])

def body_question_answering():
    """Streamlit page for question answering
       takes a string and analyses its sentiment
       also acesses database for using historical queries
    """
    # question_answering = MLQA
    pass
