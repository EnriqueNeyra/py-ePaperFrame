from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return '''
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
    '''


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    filepath = f"/home/enriquepi/repos/pic/{file.filename}"
    file.save(filepath)
    return f"File uploaded to {filepath}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
