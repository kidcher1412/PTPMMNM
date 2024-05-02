import pymsgbox
import sys

class Message:
    def show_message(self, message,timeout=4000):
        pymsgbox.confirm(message, 'Message', ["ok"], timeout=4000)