import logging.config
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threaded.file_downloader import FileDownloader
from threaded.file_monitor import FileMonitor

# Structure Logs to File System
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.config.fileConfig('logging.conf')

logger = logging.getLogger("main")

file_downloader = FileDownloader()
file_monitor = FileMonitor()


def main():
    logger.info("Started Processing")
    # Two Threads will work concurrently to monitor and download
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Concurrent Task Download
        download_future = executor.submit(file_downloader.download_ftp_server_files)
        # Concurrent Task Monitor
        monitor_future = executor.submit(file_monitor.start)
        logger.info("Download and Monitoring Services Started !!")
        for future in as_completed([download_future, monitor_future]):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")
    logger.info("Completed!!")


if __name__ == '__main__':
    main()
