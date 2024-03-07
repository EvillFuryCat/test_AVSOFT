import json
import time
from mysql.connector import connect

with open('config.json', 'r') as file:
    config_data = json.load(file)
    

host = config_data["host"]
dbname = config_data["dbname"]
user = config_data["user"]
password = config_data["password"]

class MySQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='utf-8')
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

def process_data(N, limit):
    with MySQL(host=host, user=user, password=password, database=dbname) as cursor:
        while True:
            query = f"SELECT word, SUM(count) as total_count, GROUP_CONCAT(url_file) as urls FROM word_counts GROUP BY word ORDER BY word LIMIT {limit}"
            cursor.execute(query)

            words_to_delete = []
            for word, total_count, urls in cursor:
                # print(cursor)
                if total_count > N:
                    
                    # print(f"Слово {word} встретилось {total_count} раз в файлах {urls}")
                    words_to_delete.append(word)

            for word_to_delete in words_to_delete:
                delete_query = f"DELETE FROM word_counts WHERE word = '{word_to_delete}'"
                cursor.execute(delete_query)
                # print(f"Слово {word_to_delete} удалено из базы данных")

            time.sleep(5)  

process_data(8, 10)  