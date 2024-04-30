from realtime_data import Realtime_Data
import firebase_admin
from firebase_admin import credentials, db


# Tạo một thể hiện của Realtime_Data và chuyển tham chiếu của ứng dụng Firebase cho nó
# Đường dẫn đến tệp cấu hình dịch vụ Firebase JSON
cred = credentials.Certificate("./p1_setup/connect/connect.json")
# Khởi tạo ứng dụng Firebase với tệp cấu hình
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-app-b6d6d-default-rtdb.firebaseio.com'
})

caser = Realtime_Data()
caser.ref_chat.listen(caser.handle_new_message)
caser.ref_kill.listen(caser.handle_new_message)
