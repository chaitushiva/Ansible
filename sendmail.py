import smtplib
from email.mime.text import MIMEText
import xlrd
import os
import sys
import datetime
import schedule
import time

def sendMail():
    smtp_ssl_host = 'smtp.gmail.com'  # smtp.gmail.com
    smtp_ssl_port = 465
    #username = input('USERNAME or EMAIL ADDRESS:')
    user = 'abcd'
    password = '****'
    sender = 'abcd@gmail.com'
    targets = ['efg@gmail.com', 'lmn@gmail.com'] # receipients email address and it can be any number of ids

    msg = MIMEText('*****************ALERT***********') # personalised text message
    msg['Subject'] = '************Auto-Generated Email Alert************'
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(user, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()
    print "Mail sent"


excel_file = (".\dates.xlsx") # Excel sheet name in which we have expiration column

def job(t):
    wb = xlrd.open_workbook(excel_file)
    sheet = wb.sheet_by_index(0)
    for number in range(sheet.ncols): # To get the column number of Expiration dates in Excel sheet
        # cell = str(sheet.cell_value())
        if str(sheet.cell_value(0,number))=="Expiration":
            col = number

        now = datetime.datetime.now()
        for row in range(sheet.nrows):
            expDateinExcel = str(sheet.cell_value(row, col))
            todays_date = now.strftime("%m/%d/%Y")  # Format should match as entered in the excel sheet
            if todays_date == expDateinExcel:
                sendMail()
    return

schedule.every().day.at("0:35").do(job,'It is time') #******0:35 is the time set everyday
# to execute the check and it sends mail if date is poresent in trhe expiration column

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
