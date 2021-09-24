import sqlite3

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

image_classifier_table_create_command = """CREATE TABLE IF NOT EXISTS sentiment_analysis(
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



def write_to_db(input:dict):

    text_generator_insert_query = """INSERT INTO text_generator
                                    (date, context, result) VALUES (?, ?, ?)"""
    sentiment_analysis_insert_query = """INSERT INTO sentiment_analysis
                                    (date, context, result, score) VALUES (?, ?, ?, ?)"""
    image_classifier_insert_query = """INSERT INTO image_classifier
                                    (date, filename, result, image) VALUES (?, ?, ?, ?)"""
    question_answering_insert_query = """INSERT INTO question_answering
                                    (date, context, result, score, question) VALUES (?, ?, ?, ?, ?)"""

    data_tuple = None

    try:
        database_connection = sqlite3.connect(default_db_name)
        cursor = database_connection.cursor()
        print("Connected to SQLite")

        if(input['modeltype']  == "text_generator"):
            cursor.execute(text_generator_table_create_command)
            #text_generator data tuple values [date, context, result]
            data_tuple = (input["date"], input["context"], input["result"])
            cursor.execute(text_generator_insert_query, data_tuple)
            database_connection.commit()
            cursor.close()

        elif(input['modeltype']  == "sentiment_analysis"):
            cursor.execute(sentiment_analysis_table_create_command)
            #sentiment_analysis data tuple values [date, context, result, score]
            data_tuple = (input["date"], input["context"], input["result"], input["score"])
            cursor.execute(sentiment_analysis_insert_query, data_tuple)
            database_connection.commit()
            cursor.close()

        elif(input['modeltype']  == "image_classifier"):
            cursor.execute(image_classifier_table_create_command)
            #image_classifier data tuple values [date, filename, result, image]
            data_tuple = (input["date"], input["filename"], input["result"], input["image"])
            cursor.execute(image_classifier_insert_query, data_tuple)
            database_connection.commit()
            cursor.close()

        elif(input['modeltype']  == "question_answering"):
            cursor.execute(question_answering_table_create_command)
            #question_answering data tuple values [date, context, result, score, question]
            data_tuple = (input["date"], input["context"], input["result"], input["score"], input["question"])
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
