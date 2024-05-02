import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import credentials, db

class FirestoreConnector:
    def __init__(self):
        self.db = firestore.client()
        self.ref_room = db.reference('/')
        self.list_room = []
        self.fist_run = True

    def authenticate(self, username, password):
        users_ref = self.db.collection(u'users')
        query_ref = users_ref.where(u'username', u'==', username).where(u'password', u'==', password)
        query_results = query_ref.get()
        for doc in query_results:
            user_info = doc.to_dict()
            return True, user_info
        return False, None

    def create_account(self, username, password, email):
        users_ref = self.db.collection(u'users')
        new_user_ref = users_ref.document(username)
        new_user_ref.set({
            u'username': username,
            u'password': password,
            u'email': email
        })
        print("Account created successfully!")


    def authenticate(self, username, password):
        users_ref = self.db.collection(u'users')
        query_ref = users_ref.where(u'username', u'==', username).where(u'password', u'==', password)
        query_results = query_ref.get()
        for doc in query_results:
            user_info = doc.to_dict()
            return True, user_info
        return False, None
    
    def handle_new_room(self):
        direct_children = self.ref_room.get()
        self.list_room = []
        if direct_children is not None:
            for key, val in direct_children.items():
                self.list_room.append(key)
    def create_new_room(self, ipserver):
        ipserver_key = ipserver.replace(".", "-")  # Chuyển đổi dấu chấm thành dấu gạch ngang để sử dụng làm khóa trong Firebase
        room_ref = self.ref_room.child(ipserver_key)
        room_data = room_ref.get()
        if room_data is None:
            # Nếu không có dữ liệu cho phòng này, tạo mới phòng
            room_ref.set({
                "ipserver": ipserver,
                # Các thông tin khác mà bạn muốn lưu trữ
            })
            print(f"Room with IP {ipserver} created successfully!")
        else:
            print(f"Room with IP {ipserver} already exists!")

    def delete_room(self, ipserver):
        ipserver_key = ipserver.replace(".", "-")  # Chuyển đổi dấu chấm thành dấu gạch ngang để sử dụng làm khóa trong Firebase
        room_ref = self.ref_room.child(ipserver_key)
        room_data = room_ref.get()

        if room_data is not None:
            # Nếu có dữ liệu cho phòng này, xóa nó
            room_ref.delete()
            print(f"Room with IP {ipserver} deleted successfully!")
        else:
            print(f"Room with IP {ipserver} does not exist!")
