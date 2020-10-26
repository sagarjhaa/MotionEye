from grpc_tools import protoc


# Need to understand the protoc.main function
protoc.main(
    (
        "",
        "-I.",
        "--python_out=.",
        "--grpc_python_out=.",
        "--grpc_js_out=.",
        "fileupload.proto",
    )
)
