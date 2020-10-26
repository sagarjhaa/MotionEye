import fileupload_pb2
import fileupload_pb2_grpc

import grpc
import time
import os
from os import listdir
from os.path import isfile, join
import logging

PATH = "/home/pi/Desktop/grpcTest/photos/"
DATE_FOLDER = "2020-10-25/"

import base64


def processImage(path):
    with open(path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return my_string


def uploadFile(message, stub):
    try:
        response = stub.UploadFile(request=fileupload_pb2.IncomingFile(message=message))
        return response.message
    except Exception as e:
        logging.error(e)
        time.sleep(10)


def keepChecking(stub):
    while True:
        onlyfiles = [
            f
            for f in listdir(PATH + DATE_FOLDER)
            if isfile(join(PATH + DATE_FOLDER, f))
        ]

        if len(onlyfiles) > 0:
            for file in onlyfiles:
                file_path = "{}{}{}".format(PATH, DATE_FOLDER, file)

                imageString = processImage(file_path)

                response = uploadFile(message=imageString, stub=stub)

                logging.info("Processed file " + file + " " + str(response))

                os.remove(file_path)

            time.sleep(10)


def main():
    channel = grpc.insecure_channel("192.168.0.8:2000")
    stub = fileupload_pb2_grpc.FileUploadStub(channel=channel)
    keepChecking(stub)


if __name__ == "__main__":
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(
        format=FORMAT, filename="fileupload.log", encoding="utf-8", level=logging.DEBUG
    )
    logging.info("Starting the client")
    main()