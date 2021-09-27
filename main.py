import sqlite3
import streamlit as st
import pandas as pd
from streamlit.elements import select_slider
from utilities import *

# #Remove comment to enable debug in VScode though ptvsd is needed through pip install
# import ptvsd
# print("Waiting for debugger attach")
# ptvsd.enable_attach(address=("localhost", 5678), redirect_output=True)
# ptvsd.wait_for_attach()

def body_sidebar():
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
            st.session_state['server_pid'] = ml_server.p.pid
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

def body_image_classifier():
    image_classifier = MLImageClassifier()
    classify = False
    if 'image_classes' not in st.session_state:
        st.session_state['image_classes'] = {}

    if st.session_state['running_model'] != "image_classifier":
        st.session_state['running_model'] = image_classifier.start()

    col1, col2 = st.columns([10, 10])
    with col1:
        st.header("Image Classifier")
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

        upload = st.file_uploader("Image", type=[".jpg", ".jpeg", '.png'])
        btn_classify = st.button("Classify Image")
        container = st.container()

        with st.form("Forms with things"):
            btn_update_log = st.form_submit_button("Update Log")
            regenerate_id = st.text_input("Input Id to classify")
            btn_classify_table = st.form_submit_button("Run Regeneration")

        if btn_update_log:
            db = sqlite3.connect("main_database.db")
            df = pd.read_sql("SELECT * FROM image_classifier", db)
            db.close()
            st.write(df)

        if btn_classify_table:
            db = sqlite3.connect("main_database.db")
            cur = db.cursor()
            cur.execute(f'''SELECT image,filename
                            FROM image_classifier
                            WHERE id == '{regenerate_id}' ''')
            file = cur.fetchall()
            if file != []:
                upload = file[0][0]
                classify = True
                db.close()
            else:
                st.write("Database index out of range")

        with container:
            if btn_classify or classify:
                if upload is not None:
                    if btn_classify:
                        file = upload.getvalue()
                        out = image_classifier.classify_image(file,
                                                                st.session_state["image_classes"],
                                                                upload.name)
                    elif classify:
                        out = image_classifier.classify_image(upload,
                                                                st.session_state["image_classes"],
                                                                file[0][1])
                    write_to_db(out)
                    result_dict = dict(image_classifier.r.json())
                    best_match = sorted(result_dict, key=result_dict.get, reverse=True)[0]
                    st.text(f"From the classes the best match is: {best_match.capitalize()}")
                    st.text(f"with a probability of {round(float(result_dict[best_match])*100,1)}%")
                    classify = False
    with col2:
        if upload is not None:
            st.image(upload)

def body_text_generator():
    text_generator = MLTextGenerator()
    st.header("text generator")
    if st.session_state['running_model'] != "text_generator":
        st.session_state['running_model'] = text_generator.start()
    user_input = st.text_input("Enter text you program to generate further text on")

    col1, col2, col3 = st.columns(3)
    with col1:
        text_generator_button = st.button("Generate")
    with col2:
        text_logger_button = st.button("Show log")
    with col3:
        retreive_from_log = st.button("retrieve")

    if text_generator_button:
        user_result = text_generator.get_text_gen(user_input)
        write_to_db(user_result)
        text_generator.r.json()
        duser_result = dict(text_generator.r.json())

        st.write(duser_result["generated_text"])
    if text_logger_button:
        db = sqlite3.connect("main_database.db")
        df = pd.read_sql("SELECT * FROM text_generator", db)
        db.close()
        st.write(df)
    if retreive_from_log:
        st.write("This functions is not working yet!")

    else:
        st.write("Database index out of range")


def body_sentiment_analysis():
    sentiment_analysis = MLSentimentAnalysis()
    st.header("Sentiment analysis")
    if st.session_state['running_model'] != "sentiment_analysis":
        st.session_state['running_model'] = sentiment_analysis.start()
    user_input = st.text_input("Enter text you want to analyse")
    if user_input:
        user_result = sentiment_analysis.analyse_sentiment(str(user_input))
        st.write(str(round(user_result["score"]*100,1)) + "%", user_result["result"])
        write_to_db(user_result)

def body_question_answering():
    question_answering = MLQA

def main():
    selected_model = body_sidebar()

    if selected_model == "image_classifier":
        body_image_classifier()

    elif selected_model == "sentiment_analysis":
        body_sentiment_analysis()
    elif selected_model == "text_generator":
        body_text_generator()
    elif selected_model == "question_answering":
        body_question_answering()


if __name__ == "__main__":
    st.set_page_config(page_title="Group 2 ML interactor",
                        page_icon=None,
                        layout='wide',
                        initial_sidebar_state='auto')
    main()
