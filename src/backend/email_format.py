import smtplib
import imaplib
import email
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


# def read_emails(server, email_id, password, mailbox='INBOX', email_criteria='UNSEEN'):
#     while True:
#         emails=[]
#         mail = imaplib.IMAP4_SSL(server)
#         mail.login(email_id, password)
#         mail.select(mailbox)

#         status, email_ids = mail.search(None, email_criteria)
#         if status != 'OK':
#             print("No emails found!")
#             return

#         for e_id in email_ids[0].split():
#             status, data = mail.fetch(e_id, '(RFC822)')
#             if status != 'OK':
#                 print("Error fetching the email")
#                 continue

#             # parse the email content
#             email_msg = email.message_from_bytes(data[0][1])
#             sender=(f"From: {email_msg['from']}")
#             subject=(f"Subject: {email_msg['subject']}")

#             if email_msg.is_multipart():
#                 for part in email_msg.walk():
#                     if part.get_content_type() == "text/plain":
#                         content=(part.get_payload(decode=True).decode())
#             else:
#                 content=(email_msg.get_payload(decode=True).decode())

#             emails.append({'from': sender, 'subject': subject, 'body': content})
        

        
        # mail.close()
        # mail.logout()
        # return emails

def read_emails(server, email_id, password, mailbox='INBOX', email_criteria='UNSEEN'):
    # while True:
        emails = []
        mail = imaplib.IMAP4_SSL(server)
        mail.login(email_id, password)
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
            emails.append({'from': sender, 'subject': subject, 'body': content})
            return emails

class model:
    def __init__(self, model_path="model"):
        self.model_path = "model"  # The directory should contain pytorch_model.bin and other necessary files
        self.classifier = pipeline('text-classification', model=model_path)
    
    def predict(self, text):
        return self.classifier(text[:512])
    

class Email:
    def __init__(self, sender, subject, body, original_message):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.original_message = original_message

        extractor = urlextract.URLExtract()
        urls = extractor.find_urls(self.body)
        self.links = [self.analyze_url(url) for url in urls]

        self.smtpServer = 'smtp.gmail.com'
        self.user = 'phishnetcombatant@gmail.com'
        self.password = 'tfen yldy bojq fujw'
        self.prediction= self.get_prediction()[0]

    def get_prediction(self):
        return model().predict(self.body)
    

    def analyze_url(self, url):
        url=(f"https://www.ipqualityscore.com/api/json/url/GgYkUjBka1HqmkaMCoBfflvnmzySgghJ/{quote(url, safe='')}")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404)

            return json.loads(response.text) # Return the content of the response as a string

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def checkEmailAddress(self):
        url=(f"https://www.ipqualityscore.com/api/json/email/GgYkUjBka1HqmkaMCoBfflvnmzySgghJ/{self.sender.split(' ')[-1]}")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404)

            return json.loads(response.text) # Return the content of the response as a string

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None        
        # return json.loads(requests.get(url).text)
    
    def reply(self, html_message):
        # Create an HTML message
        msg = MIMEText(html_message, 'html')
        msg['Subject'] = self.subject.replace("Subject: ", "")
        msg['From'] = self.user.replace("To: ", "")
        msg['To'] = self.original_message['from']

        # Set In-Reply-To and References headers for threading
        if 'Message-ID' in self.original_message:
            msg['In-Reply-To'] = self.original_message['Message-ID']
            msg['References'] = self.original_message['Message-ID']

        # Send the message via local SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.user, self.password)
            smtp_server.sendmail(self.user, self.original_message['from'], msg.as_string())

        print("Email sent to", self.original_message['from'])


    def format_links_info(self):
        # Start the HTML layout table
        html = "<table><tr>"
        keep=['redirected', 'suspicious','malware','phishing','category']
        # Loop through each JSON object and create a table for each
        for i, data in enumerate(self.links):
            html += f"<td><table border='1'><tr><th>Link{i+1}</th><th>{data['final_url']}</th></tr>"  # Each table in its own cell
            for key, value in data.items():
                if key not in keep:
                    continue

                # if key=='status_code':
                #     value=f"{value} ({requests.status_codes._codes[value][0]})"
                html += f"<tr><td>{key}</td><td>{value}</td></tr>"
            html += "</table><br>"

        # Close the layout table tag
        html += "</tr></table>"

                # texts=""
        # for i, link in enumerate(self.links):
        #     texts+=str(i+1)+":\n"
        #     for key, value in link.items():
        #         texts+=(f"{key}: {value}\n")
        
        return html
        
    def format_email_info(self):
        # Start the HTML layout table
        html = "<table><tr>"
        keep=['disposable','leaked']
        content=self.checkEmailAddress()
        print(content['sanitized_email'])
        html += f"<td><table border='1'><tr><th>Sender Email</th><th>{content['sanitized_email'][1:]}</th></tr>"  # Each table in its own cell
        for key, value in content.items():
            if key not in keep:
                continue
            html += f"<tr><td>{key}</td><td>{value}</td></tr>"
        html += "</table><br>"

        # Close the layout table tag
        html += "</tr></table>"
        
        return html

    def __str__(self):
        return f"{self.sender}\n{self.subject}\n{self.body}"
    


# smtpServer = 'smtp.gmail.com'
# user = 'phishnetcombatant@gmail.com'
# password = 'tfen yldy bojq fujw'

# newEmails=read_emails('imap.gmail.com', user, password, email_criteria='UNSEEN')

# e=newEmails[-1]
# e=Email(e['from'], e['subject'], e['body'])
# print(e)
# confidence_percentage = e.prediction['score'] * 100
# # e.reply(
# # f"<p>Phishnet Combatant is {confidence_percentage:.1f}% confident that this is a {e.prediction['label']}.</p>"+
# # f"<p>{len(e.links)} links were found in this email.\n</p>"+
# # e.format_links_info()
# # e.format_email_info()
#         # )       
# print(e.checkEmailAddress())
# print(e.format_links_info())