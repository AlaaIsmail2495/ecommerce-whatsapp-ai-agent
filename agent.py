import os
from typing import Dict
from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import ALL_STORE_TOOLS

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not api_key :
    raise RuntimeError("GEMINI_API_KEY is not set in your .env file.")

client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1beta"}
)

# Maintain stateful chat sessions per customer Whatsapp ID
customer_sessions: Dict[str, any] = {}

def get_or_create_chat(customer_id: str) :
    """Retrieve existing chat session or create new one with store tools enabled."""
    if customer_id not in customer_sessions :
        config = types.GenerateContentConfig(
            tools=ALL_STORE_TOOLS,
            system_instruction=(
                f"You are the official Whatsapp assistant for E-commerce Tech Store.\n"
                f"You are talking with customer, '{customer_id}'.\n"
                f"Guidelines\n"
                f"1. Help the customer browse categories, search products, check stock, add items to cart, checkout, and track orders.\n"
                f"2. When adding to cart or checking out , use the customer identifier '{customer_id}'.\n"
                f"3. Always reply in the same language as the customer (if Arabic, reply in clear, natural Arabic: if English, reply in clear, natural English).\n"
                f"4. Keep replies concise, polite, and formatted nicely for Whatsapp (use *bold* forproduct names, order IDs, and price).\n"
            ),
            temperature=0.1
        )

        chat = client.chats.create(
            model=model_name,
            config=config
        )
        customer_sessions[customer_id] = chat
    return customer_sessions[customer_id]



def process_customer_message(customer_id: str, message_text: str) ->str :
    """Send customer message to Gemini agent and return tool-resolved answer."""
    try:
        chat = get_or_create_chat(customer_id)
        response = chat.send_message(message_text)
        return response.text or  "I could not process your request at this moment."

    except Exception as e:
        return f"Error communicating with store assistant: {str(e)}"

