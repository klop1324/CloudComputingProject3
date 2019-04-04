import os
import re

from werkzeug.utils import secure_filename
import paramiko
import config as Config
from flask import url_for
import uuid
import pymysql as conn

config = Config.Config

connection = conn.connect(host=config.DB_HOST,
                          user=config.DB_USER,
                          password=config.DB_PASS,
                          db=config.DB_DATABASE,
                          charset='utf8mb4',
                          cursorclass=conn.cursors.DictCursor)

# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(config.FTP_IP, config.FTP_USERNAME, key_filename=config.FTP_PASSFILE)


def uploadFileToOtherServer(fileLocation):
    # sftp = client.open_sftp()
    # absPath = os.path.abspath(fileLocation)
    # sftp.put(absPath, absPath)
    # sftp.close()
    return


def uploadFile(file, title, author):
    fileLocation = create_file_with_random_filename(file)
    # fileURL = fileLocation[1:]
    uploadFileInfoToDB(fileLocation, title, author)
    uploadFileToOtherServer(fileLocation)
    return


def uploadFileInfoToDB(fileURL, title, author):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Pictures` (`Title`, `URI`, `Author`) " \
                  "VALUES (%s, %s, %s)"
            cursor.execute(sql, (title, fileURL, author))

        connection.commit()
    finally:
        return


def fetchPictures():
    rows = []
    try:
        with connection.cursor() as cursor:
            sql = "SELECT *" \
                  "FROM Pictures"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows

    finally:
        return rows


class PictureData(object):
    title = ""
    author = ""
    uri = ""


def getPictures():
    rows = fetchPictures()
    res = []
    for row in rows:
        item = PictureData()
        item.title = row["Title"]
        item.author = row["Author"]
        item.uri = row["URI"]
        res.append(item)
    return res


def create_file_with_random_filename(file):
    fileName = re.sub('[^A-Za-z0-9.]+', '', file.filename)
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), secure_filename(fileName)])
    fileLoc = os.path.join(config.UPLOAD_FOLDER, random_file_name)
    file.save(fileLoc)
    return fileLoc
