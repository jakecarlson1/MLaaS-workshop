import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def SendText(image, to):
    FROM = "smuimagestyle@gmail.com"
    #TO = '3038153710@mms.att.net'
    msg = MIMEMultipart()
    msg['Subject'] = 'Response'
    msg['From'] = FROM
    msg['To'] = to

    text = MIMEText("Hello, World")
    msg.attach(text)
    msg.attach(image)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(FROM, "seniordesign")
    s.sendmail(FROM, to, msg.as_string())
    s.quit()

#SendText()
