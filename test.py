import firebase_admin
from firebase_admin import credentials, db
import threading
import time

# Đường dẫn đến tệp cấu hình dịch vụ Firebase JSON
cred = credentials.Certificate("./p1_setup/connect/connect.json")
# Khởi tạo ứng dụng Firebase với tệp cấu hình
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-app-b6d6d-default-rtdb.firebaseio.com'
})

# Tham chiếu đến nút trong Realtime Database
ref_message = db.reference('IDROOM/Message')
ref_kill = db.reference('IDROOM/Kill')

def send_message(sender, content):
    """Gửi một tin nhắn mới đến Realtime Database."""
    message_data = {
        'sender': sender,
        'content': content
    }
    ref_message.push(message_data)

def send_kill(sender):
    """Gửi một tin nhắn mới đến Realtime Database."""
    message_data = {
        'sender': sender,
    }
    ref_kill.push(message_data)

# Tạo một luồng riêng để lắng nghe tin nhắn
# listener_thread = threading.Thread(target=listen_for_messages)
# listener_thread.daemon = True
# listener_thread.start()

"""Nhập tên người gửi và nội dung tin nhắn từ người dùng và gửi tin nhắn."""
# sender = input("Enter sender name: ")
# while True:
#     content = input("Enter message content: ")
#     send_message(sender, content)


"""Nhập tên người gửi tin nhan da chet."""
sender = "test"
send_kill(sender)