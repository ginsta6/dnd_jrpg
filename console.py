import pygame 

class Console:
    def __init__(self):
        self.messages = []

    def log(self, text):
        self.messages.append(text)
        if len(self.messages) > 20:
            self.messages.pop(0)

    def get_messages(self):
        return self.messages
    
    def clear(self):
        self.messages = []