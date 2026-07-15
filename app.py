return jsonify({
    "message":"File Uploaded Successfully",
    "Rows":len(df),
    "Columns":list(df.columns)
})
