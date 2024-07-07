import logging
import os
import shutil
from pprint import pprint

import parser
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config.config import LOCAL_FOLDER, TRASH_FOLDER

logger = logging.getLogger("root")


class FileHandler(FileSystemEventHandler):
    def __init__(self, process_function):
        self.process_function = process_function

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.xml'):
            print(f"File created: {event.src_path}")
            self.process_function(event.src_path)


class FileMonitor:
    def __init__(self):
        self.local_folder = LOCAL_FOLDER
        self.trash_folder = TRASH_FOLDER
        os.makedirs(self.trash_folder, exist_ok=True)

    def start(self):
        logger.info("Starting FileMonitor Threaded Service !!")
        event_handler = FileHandler(self.process_file)
        observer = Observer()
        observer.schedule(event_handler, self.local_folder, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping FileMonitor due to keyboard interrupt.")
            observer.stop()
        except Exception as e:
            logger.error(f"Unexpected error in FileMonitor: {e}")
        observer.join()

    def process_file(self, filepath):
        logger.info(f"Processing file: {filepath}")
        try:
            data_dict = parser.parse_and_extract(filepath)
            logger.debug(f"Processed {os.path.basename(filepath)}")
            pprint(data_dict)
            shutil.move(filepath, os.path.join(self.trash_folder, os.path.basename(filepath)))
            logger.info(f"Moved {os.path.basename(filepath)} to {self.trash_folder}")
            time.sleep(10) # Slow down to show logs
        except FileNotFoundError as fnf_error:
            logger.error(f"File not found: {filepath} - {fnf_error}")
        except PermissionError as perm_error:
            logger.error(f"Permission denied: {filepath} - {perm_error}")
        except Exception as e:
            logger.error(f"Error processing file {filepath}: {e}")
