import pygame


class Console:
    def __init__(self):
        self.messages = []

    def log(self, text):
        """Log a message to the console."""
        self.messages.append(text)
        if len(self.messages) > 20:
            self.messages.pop(0)

    def get_messages(self):
        """Return the messages in the console."""
        return self.messages

    def clear(self):
        """Clear the console."""
        self.messages = []
