import os
import json
from uuid import uuid4
from glob import glob

from packages.api.constants import NOTES_DIR


def get_notes():

    fichiers = glob(os.path.join(NOTES_DIR, "*.json"))
    notes = []
    for fichier in fichiers:
        with open(fichier, "r")as f:
            note_data = json.load(f)
            note_uuid = os.path.splitext(os.path.basename(fichier))[0]
            note_title = note_data.get("title")
            note_content = note_data.get("content")
            n = Note(uuid=note_uuid, title=note_title, content=note_content)
            notes.append(n)
    return notes


class Note:

    def __init__(self, title="", content="", uuid=None):
        self.title = title
        self.content = content
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = str(uuid4())

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.title}/{self.content}"


    
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise TypeError("Wrong Value")

    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True

    @property
    def path(self):
        return os.path.join(NOTES_DIR, self.uuid+".json")

    def save(self):
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

        data = {"title": self.title, "content": self.content}

        with open(self.path, "w")as f:
            json.dump(data, f, indent=4)



if __name__ == '__main__':

    note = get_notes()
    print(note)

