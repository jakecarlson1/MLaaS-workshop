import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def SendText(text, to):
    FROM = "smuimagestyle@gmail.com"
    msg = MIMEMultipart()
    
    msg['From'] = FROM
    msg['To'] = to

    text = MIMEText(text)
    msg.attach(text)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(FROM, "seniordesign")
    s.sendmail(FROM, to, msg.as_string())
    s.quit()

def SendImage(image, to):
    FROM = "smuimagestyle@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = FROM
    msg['To'] = to
    msg.attach(image)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(FROM, "seniordesign")
    s.sendmail(FROM, to, msg.as_string())
    s.quit()
