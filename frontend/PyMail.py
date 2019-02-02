#!/usr/bin/env python
import imaplib2
import datetime
from threading import *
import email
from email.mime.image import MIMEImage
import Text
import time
import os
import BackendQuery
from PIL import Image
import numpy as np

M = None
idler = None
thread = None

def stylize_and_respond(image_name, image_save_name, sender):
    try:
        image = Image.open(image_save_name).resize((720, 720), resample=Image.BICUBIC)
        image_arr = np.array(image).astype(np.float32)[:,:,:3]
        stylized = BackendQuery.style_transfer(image_name, image_arr.tostring())
        Text.SendImage(stylized, sender)
        print("Response Sent for Image: " + image_name)
    except:
        Text.SendText("An error occurred while trying to stylize your image.", sender)
    return None

def check():
    try:
        process_inbox()
    except Exception as e:
        print(e)

def process_inbox():
    # Filter to select only unread emails
    rv, data = M.search(None, "(UNSEEN)")
    if rv != 'OK':
        print("No Messages Found!")
        return

    # For every unread email
    for num in data[0].split():

        # Load up the email
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("Error getting message ", num)
            return

        email_message_instance = email.message_from_string(data[0][1])
        sender = email_message_instance['From']

        for part in email_message_instance.walk():
            if part.get_content_maintype() != 'multipart' and ("image" in str(part.get_content_type())) and part.get('Content-Disposition') is not None:
                print("Text Contains an Image")

                image_name = str(part.get_filename())
                print("Image Name: " + image_name)

                # Load the Image
                image_payload = part.get_payload(decode=True)

                # Save the Image
                now = datetime.datetime.now().isoformat()
                image_save_name = image_name.split('.')
                image_save_name = "images/" + image_save_name[0] + "__" + now + "." + image_save_name[1]
                open(image_save_name, 'wb').write(image_payload)

                # Query the style transfer service and send back the stylized image
                stylize_and_respond(image_name, image_save_name, sender)

        # Delete the email
        M.store(num, '+FLAGS', '\\Deleted')

    # Leave the inbox
    M.expunge()
    print("Done Processing Inbox")


def dosync():
    print("Got a Text")
    check()

def idle():
    needsync = True
    while True:
        if event.isSet():
            return
            needsync = False

        def callback(args):
            if not event.isSet():
                needsync = True
                event.set()

        M.idle(callback=callback)
        event.wait()
        if needsync:
            event.clear()
            dosync()

config = open('config.dat', 'r')
sender = config.readline()
emailPass = config.readline()

# Login
M = imaplib2.IMAP4_SSL('imap.gmail.com')
M.login(sender, emailPass)
M.select("inbox")
check()

#init
thread = Thread(target=idle)
event = Event()

#start
thread.start()

time.sleep(60*60)

#stop
event.set()

#join
thread.join()

M.expunge()
M.close()
M.logout()
print("DONE!")
