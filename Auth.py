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
        for key, val in direct_children.items():
            self.list_room.append(key)
# Sử dụng FirestoreConnector để tạo tài khoản
#==============
# firestore_connector = FirestoreConnector()

# # Thực hiện tạo tài khoản
# username = input("Enter username: ")
# password = input("Enter password: ")
# email = input("Enter email: ")
# firestore_connector.create_account(username, password, email)

# # Sử dụng FirestoreConnector để xác thực đăng nhập
# firestore_connector = FirestoreConnector()

# # Thực hiện xác thực đăng nhập
# username = input("Enter username: ")
# password = input("Enter password: ")
# authenticated, user_info = firestore_connector.authenticate(username, password)

# if authenticated:
#     print("Login successful!")
#     print("User information:", user_info)
# else:
#     print("Login failed. Invalid username or password.")