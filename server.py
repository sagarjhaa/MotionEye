import fileupload_pb2
import fileupload_pb2_grpc
import grpc
from concurrent import futures
import base64
import logging


class FileUploadServicer(fileupload_pb2_grpc.FileUploadServicer):
    def __init__(self):
        self.count = 0

    def UploadFile(self, request, context):
        self.count += 1
        try:
            if len(request.message) > 0:
                self.saveFile(request.message, self.count)
        except Exception as e:
            print(e)
        return fileupload_pb2.ReturnValue(message="Image processed")

    def saveFile(self, image, count):
        filename = "Image-" + str(count) + ".jpg"
        f = open("images/" + filename, "w")
        # f.write(str(image).decode("base64"))
        # f.write(str(image).decode("base64"))  # zero bytes
        # f.write(str(image))  # zero bytes
        if len(image) > 0:
            f.write(image.decode("base64"))
            print(filename + " written")

        # f.write(image)
        f.close()


def main():

    # create a grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fileupload_pb2_grpc.add_FileUploadServicer_to_server(FileUploadServicer(), server)

    server.add_insecure_port("[::]:2000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
