#!/usr/bin/env python
import imaplib2
import datetime
from threading import *
import email
from email.mime.image import MIMEImage
import Text
import time
import os

M = None
idler = None
thread = None

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
                image_save_name = image_save_name[0] + "__" + now + "." + image_save_name[1]
                open("images/" + image_save_name, 'wb').write(image_payload)

                # Prepare the Image as a MIMEImage object with a name
                image = MIMEImage(image_payload)
                image.add_header('Content-Disposition', "attachment; filename= %s" % image_name)
                Text.SendText(image, sender)
                print("Response Sent for Image: " + image_name)

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
