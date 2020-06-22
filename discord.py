import json
import sys
from datetime import datetime

class Message:
    """Class to read message dictionaries from Discord message dictionary 
    objects and create attributes from dictionary items."""

    def __init__(self, msg: dict):
        """Initialize Message object by adding each key/value pair as an 
        attribute."""

        for key, value in msg.items():
            setattr(self, key, value)
        self.data = msg
        self.dt = datetime.fromisoformat(self.timestamp)

    def __repr__(self):
        """Return dictionary of object attributes and their values."""
        return f'Message: {vars(self)}'
            
    def __str__(self):
        time = datetime.strftime(self.dt, '%Y-%m-%d %H:%M:%S')
        author = self.author.get('username')
        text = self.content
        attach = ', '.join(a.get('filename') for a in self.attachments)
        return f'{time}\t{author}\t"{text}"\t{attach}'

class Discussion(Message):
    """Class to extract messages from Discord discussion JSON files."""

    def __init__(self, json_file: str):
        """Initialize discussion object by opening JSON file and creating a 
        list of Message objects stored in the messages attribute.  The original
        data is accessible through the data attribute."""

        # Open JSON file and create attribute with JSON data
        with open(json_file, 'r') as f:
            self.file_name = f.name
            self.data = json.load(f)
        
        self.messages = []
        for msg in self.data:
            self.messages.append(Message(msg))

    def __repr__(self):
        return f'Discussion: {self.file_name} ({len(self.messages)} messages)'

    def __str__(self):
        return f'{self.file_name} contains {len(self.messages)} messages'

    def __len__(self):
        return len(self.messages)

def main():
    print(sys.argv[1])
    discussion = Discussion(sys.argv[1])
    for msg in reversed(discussion.messages):
        print(msg)

if __name__ == "__main__":
    main()
