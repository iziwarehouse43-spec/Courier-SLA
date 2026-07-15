from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({
        "message": "Courier SLA API Running"
    })

@app.route("/upload", methods=["POST"])
def upload_excel():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_excel(filepath)

    return jsonify({
        "rows": len(df),
        "columns": list(df.columns),
        "message": "Excel Uploaded Successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)
