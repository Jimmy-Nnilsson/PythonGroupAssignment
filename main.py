import streamlit as st
from utilities import *



def main():

    if 'server_pid' not in st.session_state:
        st.session_state['server_pid'] = 0
    if 'server_state' not in st.session_state:
        st.session_state['server_state'] = "Server Stopped"
    if 'image_classes' not in st.session_state:
        st.session_state['image_classes'] = {}

    ml_server = MLModel()
    image_classifier = MLImageClassifier()

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
    ml_model = st.sidebar.selectbox("Select ML Model", ["question_answering", "text_generator", "sentiment_analysis", "image_classifier"])

    if ml_model == "image_classifier":
        st.header("Image Classifier")
        btn_start = st.button("Start ML model")
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
        if upload is not None:
            st.sidebar.image(upload)
        btn_classify = st.button("Classify Image")

        if btn_start:
            image_classifier.start()

        if btn_classify:
            if upload is not None:
                out = image_classifier.classify_image(upload, st.session_state["image_classes"], upload.name)

                st.text(out["result"])
    elif ml_model == "sentiment_analysis":
        st.header("Sentiment analysis")
        a = MLSentimentAnalysis()
        a.start()

        user_input = st.text_input("label goes here", default_value_goes_here)
        st.header("MLModel")
        result = a.analyse_sentiment(user_input)
        st.text(result.get(user_input))
if __name__ == "__main__":
    srv_state = ""
    main()
