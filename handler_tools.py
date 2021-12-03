import os
import telegram
import logging
import time

from dotenv import load_dotenv
from google.cloud import dialogflow

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
                text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
            session=session, query_input=query_input)

    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text

class MyLogsHandler(logging.Handler):
    def emit(self, record):
        telegram_token_information_message = os.environ['telegram_token_information_message']
        chat_id_information_message = os.environ['chat_id_information_message']
        log_entry = self.format(record)
        bot_error = telegram.Bot(token=telegram_token_information_message)
        bot_error.send_message(chat_id=chat_id_information_message, text=log_entry)
