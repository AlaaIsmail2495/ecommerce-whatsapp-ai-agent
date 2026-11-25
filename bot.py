import os
from dotenv import load_dotenv
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv
from agent import process_customer_message 

load_dotenv()

SESSION_NAME = os.getenv("WHATSAPP_SESSION_NAME", "store_bot_session.sqlite")

# Initialize Neonize Whatsapp client
client = NewClient(SESSION_NAME)

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
    print("=======================================================")
    print("WhatsApp store bot connected successfully!")
    print("Ready to rececive and answer customer orders via AI tools.")
    print("=======================================================")


@client.event(PairStatusEv)
def on_pair_status(client: NewClient, event: PairStatusEv):
    print(f"WhatsApp Pairing Status: ID={event.ID}, Role={event.Role}")


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    # Ignore messages sent by bot itself
    if message.Info.MessageSource.IsFromMe :
        return 

    # Extract text message content
    text = ""
    if message.Message.HasField("conversation") :
        text = message.Message.conversation
    elif message.Message.HasField("extendedTextMessage") :
        text = message.Message.extendedTextMessage.text

    if not text or not text.strip() :
        return


    chat_target = message.Info.MessageSource.Chat
    customer_id = getattr(chat_target, "User", None) or str(chat_target)

    print(f"\n[WhatsApp Incoming] Customer ({customer_id}): {text}")

    # Process query with Gemini Store Agent and live backend tools
    reply_text = process_customer_message(customer_id, text)

    print(f"[WhatsApp Outgoing] Bot Reply:\n{reply_text}\n")

    # Send response back to the customer on WhatsApp
    client.send_message(chat_target, reply_text)


def start_bot():
    print("Starting WhatsApp Store Bot...")
    print("If not already paired, scan the QR code displayed in your treminal with WhatsApp.") 
    client.connect()


if __name__ =='__main__':
       start_bot()
       