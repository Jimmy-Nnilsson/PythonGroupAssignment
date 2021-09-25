import sqlite3
import streamlit as st
import pandas as pd
from utilities import *


def main():
    ml_server = MLModel()
    image_classifier = MLImageClassifier()
    sentiment_starter = MLSentimentAnalysis()
    text_starter = MLTextGenerator()
    question_answering = MLQA
    classify = False

    st.set_page_config("MLModel")
    if 'server_pid' not in st.session_state:
        st.session_state['server_pid'] = 0
    if 'server_state' not in st.session_state:
        st.session_state['server_state'] = "Server Stopped"
    if 'image_classes' not in st.session_state:
        st.session_state['image_classes'] = {}

    with st.container():
        btn_start_ml = st.sidebar.button("Start ML Model Server")
        btn_stop_ml = st.sidebar.button("Stop ML Model Server")

    if btn_start_ml:
        if st.session_state['server_pid'] == 0:
            ml_server.run_server()
            st.session_state['server_pid'] = ml_server.p.pid
    if btn_stop_ml:
        if st.session_state['server_pid'] != 0:
            ml_server.st_stop_server(st.session_state['server_pid'])
            st.session_state['server_pid'] = 0

    st.sidebar.write(f"PID {str(st.session_state['server_pid'])}")
    ml_model = st.sidebar.selectbox("Select ML Model",
                                    ["question_answering",
                                     "text_generator",
                                     "sentiment_analysis",
                                     "image_classifier"])

    if ml_model == "image_classifier":
        col1, col2 = st.columns([20, 5])
        with col1:
            st.header("Image Classifier")
            btn_start = st.button("Start ML model")
            if btn_start:
                image_classifier.start()
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

            with st.expander("Model log"):
                with st.form("Forms with things"):
                    btn_update_log = st.form_submit_button("Update Log")
                    regenerate_id = st.text_input("Input Id to classify")
                btn_classify_table = st.button("Run Regeneration")

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
                    upload = file[0][0]
                    st.write(file[0][1])
                    classify = True
                    db.close()
            with container:
                if btn_classify:
                    if upload is not None:
                        file = upload.getvalue()
                        out = image_classifier.classify_image(file,
                                                              st.session_state["image_classes"],
                                                              upload.name)
                        write_to_db(out)
                        st.text(out["result"])
                        classify = False
                elif classify:
                    if upload is not None:
                        out = image_classifier.classify_image(upload,
                                                              st.session_state["image_classes"],
                                                              file[0][1])
                        write_to_db(out)
                        st.text(out["result"])
                        classify = False
        with col2:
            if upload is not None:
                st.image(upload)

    elif ml_model == "sentiment_analysis":
        st.header("Sentiment analysis")
        sentiment_starter.start()
        user_input = st.text_input("Enter text you want to analyse")
        if user_input:
            user_result = sentiment_starter.analyse_sentiment(str(user_input))
            write_to_db(user_result)
    elif ml_model == "text_generator":
        st.header("text generator")
        text_starter.start()
        user_input = st.text_input("Enter text you program to generate further text on")
        user_result = text_starter.get_text_gen(str(user_input))
        if st.button('Click here for the result'):
            st.text(user_result.get("result"))
    elif ml_model == "question_answering":
        # question_answering
        pass


if __name__ == "__main__":
    srv_state = ""
    main()
