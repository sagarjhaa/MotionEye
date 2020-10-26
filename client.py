import fileupload_pb2
import fileupload_pb2_grpc

import grpc
import time
import os
from os import listdir
from os.path import isfile, join
import logging
import json
from datetime import datetime
import base64
from common import loadConfiguration


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
        logging.info("Waiting for 10 seconds for server to startup")
        time.sleep(10)


def keepChecking(stub):
    config = loadConfiguration()
    PATH = config["images_path"]
    while True:
        try:

            DATE_FOLDER = datetime.today().strftime("%Y-%M-%d") + "/"

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

                time.sleep(config["frequency_sleep_sec"])

        except Exception as e:
            logging.error(e)


def main():
    config = loadConfiguration()

    server_addr = config["server_ip"]
    grpc_port = config["grpc_port"]

    channel = grpc.insecure_channel(server_addr + ":" + grpc_port)
    stub = fileupload_pb2_grpc.FileUploadStub(channel=channel)
    keepChecking(stub)


if __name__ == "__main__":
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(
        format=FORMAT, filename="client.log", encoding="utf-8", level=logging.DEBUG
    )
    logging.info("\n Starting the client")
    main()