# Automated File Processing
1. Used a 10-Second Interval to show the logs.
2. Did not find FTP for BI_Directional. So, used HTTP Polling
3. Reconnect to FTP if disconnected.
4. Logging (FileSystem)
5. Threaded Task (FileDownload) (FileMonitor)
6. Xml Parser to Dictionary
```shell
docker-compose up --build --force-recreate -d
docker-compose logs
```

