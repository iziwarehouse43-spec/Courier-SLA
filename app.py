@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({"error":"No file selected"})

    file=request.files["file"]

    filepath=os.path.join(UPLOAD_FOLDER,file.filename)

    file.save(filepath)

    df=pd.read_excel(filepath)

    df["Dispatch Date"]=pd.to_datetime(df["Dispatch Date"])

    today=pd.Timestamp.today()

    df["Ageing Days"]=(today-df["Dispatch Date"]).dt.days


    courier_sla={
        "BlueDart":3,
        "DTDC":5,
        "Shree Maruti":4
    }


    df["SLA Days"]=df["Shipping Courier"].map(courier_sla)

    df["SLA Status"]=df.apply(
        lambda x:
        "BREACH" if x["Ageing Days"]>x["SLA Days"]
        else "Within SLA",
        axis=1
    )


    result={
        "Total Orders":len(df),
        "SLA Breach":len(df[df["SLA Status"]=="BREACH"]),
        "Within SLA":len(df[df["SLA Status"]=="Within SLA"])
    }


    return jsonify(result)
