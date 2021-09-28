"""Group project 2
Use api to connect to machine learning models.
Store the results in a database for reuse
"""
import utilities

def main():
    """Main module
    """
    selected_model = utilities.body_sidebar()

    if selected_model == "image_classifier":
        utilities.body_image_classifier()
    elif selected_model == "sentiment_analysis":
        utilities.body_sentiment_analysis()
    elif selected_model == "text_generator":
        utilities.body_text_generator()
    elif selected_model == "question_answering":
        utilities.body_question_answering()


if __name__ == "__main__":

    main()
