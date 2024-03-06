from rabbitManager import RabbitManager
from MysqlManager import MySQL
from analyzer_parser import Parser

host = "mysql_database"
dbname = "avsoft"
user = "root"
password = "My7Pass@Word_9_8A_zE"


def main() -> None:
    rabbit_manager = RabbitManager()
    # Нужно обработать ошибки и добавить callback для rabbit
    rabbit_manager.connect_queue("Parsing")
    
    with MySQL(host=host, user=user, password=password, database=dbname) as db:
        analyzer = Parser(db)
        rabbit_manager.consume_messages("Parsing", analyzer.process_message)


if __name__ == "__main__":
    main()