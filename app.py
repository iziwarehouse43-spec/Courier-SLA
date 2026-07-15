from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return """
    <h2>Courier SLA API</h2>

    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <br><br>
        <button type="submit">Upload Excel</button>
    </form>
    """

@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({"error":"No file selected"})

    file = request.files["file"]

    filepath=os.path.join(UPLOAD_FOLDER,file.filename)

    file.save(filepath)

    df=pd.read_excel(filepath)

    return jsonify({
        "message":"File Uploaded Successfully",
        "Rows":len(df),
        "Columns":list(df.columns)
    })

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
