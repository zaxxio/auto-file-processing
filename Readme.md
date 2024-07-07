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

# Containerization
```dockerfile
version: '3.8'
services:
  ftp-base-station:
    image: fauria/vsftpd
    container_name: ftp-server
    environment:
      FTP_USER: nybsys
      FTP_PASS: 12345
    ports:
      - "20:20"
      - "21:21"
      - "21100-21110:21100-21110"
    volumes:
      - ./shared/ftp:/home/vsftpd
    networks:
      - cloudNetwork

  automated-file-processing:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: automated-file-processing
    environment:
      FTP_HOST: host.docker.internal
      FTP_USER: "nybsys"
      FTP_PASS: "12345"
      TEMP_FOLDER: "/app/temp"
      LOCAL_FOLDER: "/app/local"
      TRASH_FOLDER: "/app/trash"
    volumes:
      - ./temp:/app/temp
      - ./local:/app/local
    restart: always
    networks:
      - cloudNetwork

networks:
  cloudNetwork:
    driver: bridge
```

