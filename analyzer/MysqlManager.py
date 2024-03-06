from typing import Self
from mysql.connector import connect


class MySQL:
    def __init__(self, host, user, password, database) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __enter__(self) -> Self:
        self.connection = connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='utf-8')
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cursor.close()
        self.connection.close()

    def save_word_count(self, path: str, word: str, count: int) -> None:
        query = "INSERT INTO word_counts (url_file, word, count) VALUES (%s, %s, %s)"
        values = (path, word, count)
        self.cursor.execute(query, values)
        self.connection.commit()