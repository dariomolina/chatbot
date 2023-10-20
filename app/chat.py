import os
from abc import ABC, abstractmethod

import openai
import requests
from dotenv import load_dotenv
from fastapi import FastAPI

from context import system_context

load_dotenv()
app = FastAPI()

openai.api_key = os.getenv("OPEN_IA_KEY")


class MessageProcessor(ABC):
    @abstractmethod
    def process(self, phone_number_id, message_text):
        pass


class ChatManager(MessageProcessor):
    def __init__(self):
        self.context_dict = {}

    def process(self, phone_number_id, message_text):
        if not self.context_dict.get(phone_number_id):
            self.context_dict[phone_number_id] = [system_context]
        self.context_dict[phone_number_id].append({"role": "user", "content": message_text})
        conversation_context = self.context_dict[phone_number_id]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_context
        )
        response_content = response.choices[0].message.content
        self.context_dict[phone_number_id].append({"role": "assistant", "content": response_content})
        print(self.context_dict)
        return response_content


class ChatAPI:
    def __init__(self, message_processor: MessageProcessor):
        self.message_processor = message_processor
        self.url = os.getenv("META_URL")
        self.headers = {
            "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
            "Content-Type": "application/json"
        }

    def process_message(self, phone_number_id, message_text):
        response_text = self.message_processor.process(phone_number_id, message_text)
        return response_text

    def send_response(self, to, message_text):
        to_str = str(to)
        # fix phone number
        fix_to = int(to_str[:2] + to_str[3:])
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": fix_to,
            "type": "text",
            "text": {
                "body": message_text
            }
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        print(response)
