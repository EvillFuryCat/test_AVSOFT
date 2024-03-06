from collections import defaultdict
import re
import json


class Parser:
    def __init__(self, db) -> None:
        self.db = db

    def process_message(self, ch, method, properties, body) -> None:
        message = json.loads(body)
        path = message.get("path", "")
        
        with open(path, "r") as file:
            content = file.read()
        
        words = self.count_word_occurrences(content)
        for word, count in words.items():
            self.db.save_word_count(path, word, count)
            
            
    def count_word_occurrences(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
        return word_count
