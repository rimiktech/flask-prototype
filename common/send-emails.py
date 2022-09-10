'''
We have a program which is used to send crash report of desktop app via email with log files.
Please modify this program to send all log files instead of last log file.

'''

import yagmail
import pdb
import threading
from datetime import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import glob
from zipfile import ZipFile


class alerts:

    def __init__(self):
        self.user = "xxxxxxx"
        self.password = "xxxxxxx"
        self.to_email = "suport@xxxxxxx.com"
        self.log_path = "D:\\logs"
        

    def __send(self, subject, message, attachments = None):
        try:
            print("Sending email alert...")
            with yagmail.SMTP(self.user, self.password) as yag:
                if attachments is not None:
                    yag.send(self.to_email, subject, [message], attachments)
                else:
                    yag.send(self.to_email, subject, [message])
                print("Sent email.")
        except Exception as e:
            print("Exeception occured:{}".format(e))
            print("Sent email is failed.")
            return False
    
    
    def send_crash_report(self):
        files = [f for f in files]
        subject = "App is crashed."
        msg = """App is crashed on {0:%Y-%m-%d %H:%M:%S}. <br/> 
            Please check attached log file for detailed information."""
        msg = msg.format(datetime.now())
        
        log_files = glob.glob(self.log_path + "\\*")
        if len(log_files) == 0:
            self.__send(subject, msg, None)
            return

        with ZipFile('logs.zip', 'w') as zipObj2:
            for file in log_files:
                zipObj2.write(file)
        self.__send(subject, msg, 'logs.zip')
            
        