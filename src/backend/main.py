from email_format import Email
import imaplib
import email
import time
import re
import os
from dotenv import load_dotenv

def monitor_emails(server, email_id, password, mailbox='INBOX', email_criteria='UNSEEN'):
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
            f"Phishnet Combatant is {confidence_percentage:.1f}% confident that this is a {'safe' if e.get_prediction()[0]['label'] == 'SAVE EMAIL' else 'potentially dangerous'} email.\n"+
            f"{len(e.links)} links were found in this email.\n"+"\n"+
            e.format_links_info()+
            e.format_email_info()
                    )       

        # time.sleep(5)


smtpServer = 'smtp.gmail.com'
user = os.getenv('USER')
password = os.getenv('PASS') 

monitor_emails('imap.gmail.com', user, password, email_criteria='UNSEEN')

