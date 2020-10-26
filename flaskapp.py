from flask import Flask, render_template, request, redirect
from client import uploadFile

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("/index.html", result=result)


@app.route("/submit")
def submit():
    val = request.args["message"]
    print(f"value {val}")

    result = uploadFile(val)

    return render_template("/index.html", result=result)


if __name__ == "__main__":
    app.run()