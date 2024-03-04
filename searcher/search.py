
import json
import os
import shutil
import magic

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from rabbitManager import RabbitManager


class FileSeeker(FileSystemEventHandler):
    def __init__(self, text_file_folder: str, errors_folder: str, rabbit_manager: RabbitManager) -> None:
        super().__init__()
        # self.folder_to_watch = folder_to_watch
        self.text_file_folder = text_file_folder
        self.errors_folder = errors_folder
        self.rabbit = rabbit_manager
    
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return "ooops"
        
        file_name = event.src_path
        if 'text' in magic.from_file(file_name):
            new_path = self.move_file(file_name=file_name, directory=self.text_file_folder)
            message = json.dumps({"path": new_path})
            self.rabbit.send_message(message, "Parsing")
        else:
            new_path = self.move_file(file_name=file_name, directory=self.errors_folder)
            message = json.dumps({"path": new_path})
            self.rabbit.send_message(message, "Errors")
        
    
    def move_file(self, file_name: str, directory: str) -> None:
        new_path = os.path.join(directory, os.path.basename(file_name))
        shutil.move(file_name, new_path)
        return new_path
