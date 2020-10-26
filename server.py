import fileupload_pb2
import fileupload_pb2_grpc
import grpc
from concurrent import futures
import base64
import logging
from datetime import datetime
from common import loadConfiguration


class FileUploadServicer(fileupload_pb2_grpc.FileUploadServicer):
    def __init__(self):
        self.count = 0
        self.serverImagePath = loadConfiguration()["server_images_path"]

    def UploadFile(self, request, context):
        self.count += 1
        try:
            if len(request.message) > 0:
                self.saveFile(request.message, self.count)
            return fileupload_pb2.ReturnValue(message="Image processed")
        except Exception as e:
            logging.error(e)
            return fileupload_pb2.ReturnValue(message="Image not processed")

    def saveFile(self, image, count):
        filename = "Image - {}.jpg".format(str(count))

        file_path = self.serverImagePath + filename

        f = open(file_path, "w")
        if len(image) > 0:
            f.write(image.decode("base64"))
            logging.info("{} - written".format(filename))
        f.close()


def main():
    config = loadConfiguration()

    # create a grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fileupload_pb2_grpc.add_FileUploadServicer_to_server(FileUploadServicer(), server)

    server.add_insecure_port("[::]:" + config["grpc_port"])
    print("Server started")
    logging.info("Server started")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(
        format=FORMAT, filename="server.log", encoding="utf-8", level=logging.DEBUG
    )
    main()
