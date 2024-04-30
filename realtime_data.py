
from firebase_admin import credentials, db

class Realtime_Data():
    def __init__(self):
        # Tham chiếu đến nút trong Realtime Database
        self.ref_chat = db.reference('IDROOM/Message')
        self.ref_kill = db.reference('IDROOM/Kill')
        self.fist_run = True 
        self.list_chat = []
        self.list_kill = []
    def handle_new_message(self, event):
        """Xử lý tin nhắn mới từ Realtime Database."""
        if event.data:
            if self.fist_run:
                for key, message in event.data.items():
                    self.list_chat.append(message)
                self.fist_run = False
            else:
                self.list_chat.append(event.data)
    def handle_new_kill(self, event):
        """Xử lý tin nhắn mới từ Realtime Database."""
        if event.data:
            if self.fist_run:
                for key, message in event.data.items():
                    self.list_kill.append(message)
                self.fist_run = False
            else:
                self.list_kill.append(event.data)
                
    def send_message(self, sender, content):
        """Gửi một tin nhắn mới đến Realtime Database."""
        message_data = {
            'sender': sender,
            'content': content
        }
        self.ref_chat.push(message_data)

    def send_kill(self, sender):
        """Gửi một tin nhắn mới đến Realtime Database."""
        message_data = {
            'sender': sender,
        }
        self.ref_kill.push(message_data)

