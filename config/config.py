# Nybsys ftp server provided in the docker-compose yaml
import os

FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')
TEMP_FOLDER = os.getenv('TEMP_FOLDER')
LOCAL_FOLDER = os.getenv('LOCAL_FOLDER')
TRASH_FOLDER = os.getenv('TRASH_FOLDER', '/app/trash')
