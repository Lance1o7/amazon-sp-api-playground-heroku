from sp_api.base import Marketplaces, ReportType
from sp_api.api import Orders, Reports
from datetime import date, datetime, timedelta
import hashlib
import os

def createReportFromInput(form):
    try:
        refreshtoken = form['refreshtoken']
        appid = form['appid']
        clientsecret = form['clientsecret']
        awssecret = form['awssecret']
        awsaccess = form['awsaccess']
        rolearn = form['rolearn']
        reportPeriod = form['reportPeriod']
        distributorView = form['distributorView']
        sellingProgram = form['sellingProgram']
        reportType = form['ReportType']
        startTime = form['startTime']
        endTime = form['endTime']

        credentials = dict(
            refresh_token=refreshtoken,
            lwa_app_id=appid,
            lwa_client_secret=clientsecret,
            aws_secret_key=awssecret,
            aws_access_key=awsaccess,
            role_arn=rolearn,
        )

        reportOptions = dict(
            reportPeriod="WEEK" if reportPeriod == "1" else "DAY",
            distributorView="MANUFACTURING" if distributorView == "1" else "SOURCING",
            sellingProgram="RETAIL" if sellingProgram == "1" else "RETAIL"
        )

        if reportType == "1":
            res = Reports(credentials=credentials).create_report(
                reportOptions=reportOptions,
                reportType=ReportType.GET_VENDOR_SALES_REPORT,
                dataStartTime=startTime,
                dataEndTime=endTime,
                marketplaceIds=[
                    "ATVPDKIKX0DER"
                ])
            print(res)
            return res.payload
        else:
            res = Reports(credentials=credentials).create_report(
                reportOptions=reportOptions,
                reportType=ReportType.GET_VENDOR_INVENTORY_REPORT,
                dataStartTime=startTime,
                dataEndTime=endTime,
                marketplaceIds=[
                    "ATVPDKIKX0DER"
                ])
            #print(res)
            return res.payload
    except:
        return "Please check your input data."

def getAllReportsFromInput(form):
    try:
        refreshtoken = form['refreshtoken']
        appid = form['appid']
        clientsecret = form['clientsecret']
        awssecret = form['awssecret']
        awsaccess = form['awsaccess']
        rolearn = form['rolearn']
        report_types = ["GET_VENDOR_INVENTORY_REPORT", "GET_VENDOR_SALES_REPORT"]
        processing_status = ["IN_QUEUE", "IN_PROGRESS", "DONE", "FATAL"]

        credentials = dict(
            refresh_token=refreshtoken,
            lwa_app_id=appid,
            lwa_client_secret=clientsecret,
            aws_secret_key=awssecret,
            aws_access_key=awsaccess,
            role_arn=rolearn,
        )

        res = Reports(credentials=credentials).get_reports(reportTypes=report_types, processingStatuses=processing_status)
        #print(res)
        return res.payload

    except:
        return "Please check your input data."


def downloadAndDecryptSPE(documentID):
    f = open("report.txt", "w")
    res = Reports().get_report_document(documentID, decrypte=True, download=True, file=f)
    print(res)
    f.close()

def downloadReportFromInput(form):
    try:
        refreshtoken = form['refreshtoken']
        appid = form['appid']
        clientsecret = form['clientsecret']
        awssecret = form['awssecret']
        awsaccess = form['awsaccess']
        rolearn = form['rolearn']
        documentID = form['documentID']
        filename = hashlib.md5(documentID.encode('utf-8')).hexdigest()
        path = os.path.join(os.path.dirname(__file__),'static', filename+".json")
        f = open(path, "w")
        credentials = dict(
            refresh_token=refreshtoken,
            lwa_app_id=appid,
            lwa_client_secret=clientsecret,
            aws_secret_key=awssecret,
            aws_access_key=awsaccess,
            role_arn=rolearn,
        )
        res = Reports(credentials=credentials).get_report_document(documentID, decrypte=True, download=True, file=f)
        return res
    except:
        return "Something wrong. Please check your input."