from email_format import Email
import smtplib
import imaplib
import email
import time
from os import path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from transformers import pipeline
import urlextract
import validators
import requests
from urllib.parse import quote
import json
import re

def read_emails(server, email_id, password, mailbox='INBOX', email_criteria='UNSEEN'):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_id, password)
    print("Logged in successfully!")
    while True:
        emails = []
        mail.select(mailbox)
        status, email_ids = mail.search(None, email_criteria)
        if status != 'OK':
            print("No emails found!")
            return

        for e_id in email_ids[0].split():
            status, data = mail.fetch(e_id, '(RFC822)')
            if status != 'OK':
                print("Error fetching the email")
                continue

            # Parse the email content
            email_msg = email.message_from_bytes(data[0][1])

            # Check for forwarded email pattern
            forwarded_pattern = r"----- Forwarded message -----.*?From: (.+?)\n"

            if email_msg.is_multipart():
                for part in email_msg.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode()
                        match = re.search(forwarded_pattern, content, re.DOTALL)
                        if match:
                            sender = f"From: {match.group(1)}"
                            break
                    else:
                        sender = f"From: {email_msg['from']}"
            else:
                content = email_msg.get_payload(decode=True).decode()
                match = re.search(forwarded_pattern, content, re.DOTALL)
                if match:
                    sender = f"From: {match.group(1)}"
                else:
                    sender = f"From: {email_msg['from']}"

            subject = f"Subject: {email_msg['subject']}"
            emails.append({'from': sender, 'subject': subject, 'body': content, 'original': email_msg})

        if emails!=[]:
            e=emails[0]
            e=Email(e['from'], e['subject'], e['body'], e['original'])
            confidence_percentage = e.prediction['score'] * 100
            e.reply(
            f"<p>Phishnet Combatant is {confidence_percentage:.1f}% confident that this is a {'safe' if e.get_prediction()[0]['label'] == 'SAVE EMAIL' else 'potentially dangerous'} email.</p>"+
            f"<p>{len(e.links)} links were found in this email.\n</p>"+
            e.format_links_info()+
            e.format_email_info()
                    )       

        time.sleep(5)


smtpServer = 'smtp.gmail.com'
user = 'phishnetcombatant@gmail.com'
password = ''

read_emails('imap.gmail.com', user, password, email_criteria='UNSEEN')

