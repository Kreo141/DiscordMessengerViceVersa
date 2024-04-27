from fbchat import Client
from fbchat.models import Message, ThreadType
import requests

class SimpleMessenger(Client):
    def __init__(self, email, password, session_cookies):
        super().__init__(email, password, session_cookies=session_cookies)
        self.last_message_id = None

    def retrieve_messages_from_discord(self, channel_id):
        headers = {
            #you can find your key by using inspect element
            'authorization': 'DISCORD_AUTHORIZATION_KEY'
        }
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        params = {'after': self.last_message_id} if self.last_message_id else {}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            messages = response.json()
            if messages:
                self.last_message_id = messages[-1]['id']
            messages.reverse()
            message_texts = [message['content'] for message in messages]
            return "\n".join(message_texts)
        else:
            return "Failed to retrieve messages from Discord."

    def send_message_to_discord(self, message):
        headers = {
            'authorization': 'DISCORD_AUTHORIZATION_KEY'
        }
        payload = {
            'content': message
        } 
        response = requests.post("https://discord.com/api/v9/channels/------channel_id------/messages", data=payload, headers=headers)
        if response.status_code == 200:
            return "Message sent to Discord successfully."
        else:
            return "Failed to send message to Discord."

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        if author_id != self.uid:
            message_text = message_object.text.lower() if message_object.text else ""
            if "shazam" in message_text:
                discord_messages = self.retrieve_messages_from_discord('1233035385559580685')
                self.send(Message(text=discord_messages), thread_id=thread_id, thread_type=thread_type)
            elif message_text.startswith("discord:"):
                message_to_send = message_text.replace("discord:", "").strip()
                response = self.send_message_to_discord(message_to_send)
                self.send(Message(text=response), thread_id=thread_id, thread_type=thread_type)
            else:
                self.send(Message(text="Pooping..."), thread_id=thread_id, thread_type=thread_type)

#put your facebook login session cookies here!
session_cookies = {
    "sb": "__",
    "fr": "__",
    "c_user": "__",
    "datr": "__",
    "xs": "__"
}

client = SimpleMessenger("EMAIL", "PASS", session_cookies=session_cookies)
print(client.isLoggedIn())

try:
    client.listen()
except KeyboardInterrupt:
    print("Interrupted")
