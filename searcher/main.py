from rabbitManager import RabbitManager
from search import FileSeeker
from watchdog.observers import Observer


folder_to_watch = "../resource/search"
text_file_folder = "../resource/analyzer"
errors_folder = "../resource/errors"


def main() -> None:
    rabbit = RabbitManager()
    rabbit.create_queue("Parsing")
    rabbit.create_queue("Errors")
    
    file_handler = FileSeeker(text_file_folder, errors_folder, rabbit)
    observer = Observer()
    observer.schedule(file_handler, folder_to_watch, recursive=False)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()



if __name__ == "__main__":
    main()