import streamlit as st
from utilities import *

# #Remove comment to enable debug in VScode though ptvsd is needed through pip install
# import ptvsd
# print("Waiting for debugger attach")
# ptvsd.enable_attach(address=("localhost", 5678), redirect_output=True)
# ptvsd.wait_for_attach()

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
