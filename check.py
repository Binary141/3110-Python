#!/usr/bin/python3

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess

hosts = open(sys.argv[1], 'r')
Lines = hosts.readlines()
offline = ""
services = ""
arg = ""
whole_cmd = ""

for line in Lines:
   ip_addr = line.split(':')[0]
   srv = line.split(':')[1]

   response = os.system("ping -c 1 " + ip_addr + " >/dev/null 2>&1")

   if response == 0: #non zero number means the connection failed
       whole_cmd = 'PATH_TO_FILE/python3110.sh %s %s' %(ip_addr, srv)
       output = subprocess.check_output(whole_cmd, shell=True)

       
       print("THING: ", output)
       if "\\nactive\\n" in str(output):
            print("TRUE")
       else:
            print("OUTPUT")

   else:
       print('Host: %s is NOT up!' %ip_addr) 
       offline += ip_addr
       offline += " "
       services += srv
       services += " "
print(offline)

if len(offline) >= 1:
       mail_content = "Hello, hosts " + offline + "are offline! with the services " + services
       #The mail addresses and password
       sender_address = 'EMAIL_ADDR'
       sender_pass = 'EMAIL_PASSWD'
       receiver_address = 'EMAIL_ADDR'
       #Setup the MIME
       message = MIMEMultipart()
       message['From'] = sender_address
       message['To'] = receiver_address
       message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
       #The body and the attachments for the mail
       message.attach(MIMEText(mail_content, 'plain'))
       #Create SMTP session for sending the mail
       session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
       session.starttls() #enable security
       session.login(sender_address, sender_pass) #login with mail_id and password
       text = message.as_string()
       session.sendmail(sender_address, receiver_address, text)
       session.quit()
       print('Mail Sent')
hosts.close()
