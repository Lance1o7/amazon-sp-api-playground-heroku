from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from Service import createReportFromInput, getAllReportsFromInput, downloadReportFromInput
import json

app = Flask(__name__)


@app.route('/create', methods=['POST', 'GET'])
def createReport():
    if request.method == 'POST':
        res = createReportFromInput(request.form)
        return "Successfully create the report."
    return render_template('create.html')


@app.route('/get', methods=['POST', 'GET'])
def getAllReports():
    if request.method == 'POST':
        res = getAllReportsFromInput(request.form)
        return res
    return render_template('get.html')


@app.route('/download', methods=['POST', 'GET'])
def downloadReport():
    if request.method == 'POST':
        res = downloadReportFromInput(request.form)
        return send_file(res, as_attachment=True)

    return render_template('download.html')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    print("yes")
    app.run(debug=True)
