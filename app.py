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
        return jsonify({"error": "No file selected"})


    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)


    # Read Excel
    df = pd.read_excel(filepath)


    # Convert Dispatch Date
    df["Dispatch Date"] = pd.to_datetime(
        df["Dispatch Date"],
        errors="coerce"
    )


    today = pd.Timestamp.today()


    # Calculate ageing
    df["Ageing Days"] = (
        today - df["Dispatch Date"]
    ).dt.days


    # Courier SLA days
    courier_sla = {
        "BlueDart": 3,
        "DTDC": 5,
        "Shree Maruti": 4
    }


    df["SLA Days"] = df["Shipping Courier"].map(courier_sla)


    # SLA Status
    df["SLA Status"] = df.apply(
        lambda x:
        "BREACH"
        if x["Ageing Days"] > x["SLA Days"]
        else "Within SLA",
        axis=1
    )


    # Final Report
    result = {

        "Total Orders": len(df),

        "SLA Breach": len(
            df[df["SLA Status"] == "BREACH"]
        ),

        "Within SLA": len(
            df[df["SLA Status"] == "Within SLA"]
        )

    }


    return jsonify(result)



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
