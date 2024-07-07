import ftplib
import logging
import os
import shutil
import time
from config.config import FTP_HOST, FTP_USER, FTP_PASS, TEMP_FOLDER, LOCAL_FOLDER

logger = logging.getLogger("main")


class FileDownloader:
    def __init__(self):
        self.host = FTP_HOST
        self.user = FTP_USER
        self.password = FTP_PASS
        self.temp_folder = TEMP_FOLDER
        self.local_folder = LOCAL_FOLDER
        self.downloaded_files_path = "downloaded_files.txt"
        self.downloaded_files = self.load_downloaded_files()

        os.makedirs(self.temp_folder, exist_ok=True)
        os.makedirs(self.local_folder, exist_ok=True)

    def load_downloaded_files(self):
        if os.path.exists(self.downloaded_files_path):
            with open(self.downloaded_files_path, 'r') as f:
                return set(f.read().splitlines())
        return set()

    def save_downloaded_file(self, filename):
        self.downloaded_files.add(filename)
        with open(self.downloaded_files_path, 'a') as f:
            f.write(f"{filename}\n")

    def connect(self, retries=5, delay=5):
        attempt = 0
        while attempt < retries:
            try:
                self.ftp = ftplib.FTP(self.host)
                self.ftp.login(self.user, self.password)
                self.ftp.cwd("/")
                logger.info(f"Connected to FTP server {self.host}")
                return
            except ftplib.all_errors as e:
                attempt += 1
                logger.error(f"Failed to connect to FTP server (Attempt {attempt}/{retries}): {e}")
                time.sleep(delay)
        raise Exception("Failed to connect to FTP server after several attempts.")

    def reconnect(self, retries=5, delay=5):
        logger.info("Attempting to reconnect to FTP server...")
        self.connect(retries, delay)

    def download_ftp_server_files(self):
        while True:
            try:
                self.connect()
                while True:
                    try:
                        filenames = self.ftp.nlst()
                    except ftplib.error_perm as e:
                        logger.error(f"Failed to list files in FTP directory: {e}")
                        self.reconnect()
                        continue

                    for filename in filenames:
                        if filename in self.downloaded_files:
                            continue

                        local_filepath = os.path.join(self.temp_folder, filename)
                        if not os.path.exists(local_filepath):
                            try:
                                with open(local_filepath, "wb") as file:
                                    self.ftp.retrbinary(f"RETR {filename}", file.write)
                                logger.info(f"Downloaded {filename} to {self.temp_folder}")

                                # Move the file to the local folder
                                shutil.move(local_filepath, os.path.join(self.local_folder, filename))
                                logger.info(f"Moved {filename} to {self.local_folder}")

                                # Add to the set of downloaded files and save the record
                                self.save_downloaded_file(filename)
                            except ftplib.error_temp as e:
                                logger.error(f"Temporary FTP error for file {filename}: {e}. Retrying...")
                                self.reconnect()
                                continue
                            except ftplib.error_perm as e:
                                logger.error(f"Permanent FTP error for file {filename}: {e}. Skipping...")
                                continue
                            except IOError as e:
                                logger.error(f"File I/O error for {filename}: {e}")
                    time.sleep(3)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(5)
            finally:
                try:
                    self.ftp.quit()
                except ftplib.all_errors as e:
                    logger.error(f"Failed to close FTP connection: {e}")
