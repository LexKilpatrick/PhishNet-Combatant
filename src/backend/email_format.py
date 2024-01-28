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


class model:
    def __init__(self, model_path="src/backend/model"):
        self.model_path = "src/backend/model"  # The directory should contain pytorch_model.bin and other necessary files
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
        self.links = [self.analyze_url(url) for url in urls if 'urldefense' not in url]

        self.smtpServer = 'smtp.gmail.com'
        self.user = 'phishnetcombatant@gmail.com'
        self.password = 'tfen yldy bojq fujw'
        self.prediction= self.get_prediction()[0]

    def get_prediction(self):
        return model().predict(self.body)
    

    def analyze_url(self, url):
        url=(f"https://www.ipqualityscore.com/api/json/url/r65d0SnlG42inZOuStz6IeVS9H94nrNb/{quote(url, safe='')}")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404)

            return json.loads(response.text) # Return the content of the response as a string

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def checkEmailAddress(self):
        url=(f"https://www.ipqualityscore.com/api/json/email/r65d0SnlG42inZOuStz6IeVS9H94nrNb/{self.sender.split(' ')[-1]}")
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
        msg = MIMEText(html_message, 'plain')
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
        keep=['redirected', 'suspicious','malware','phishing','category']
        message=""
        for i, data in enumerate(self.links):
            message+=f"Domain {i+1}\n{data['domain']}\n"
            for key, value in data.items():
                if key not in keep:
                    continue
                message+=f"{key}: {value}\n"
            message+="\n"

        return message


    def format_email_info(self):
        message=""
        keep=['disposable','leaked']
        content=self.checkEmailAddress()
        message+=f"Sender Email\n{content['sanitized_email'][1:-1]}\n"
        for key, value in content.items():
            if key not in keep:
                continue
            message+=f"{key}: {value}\n"
        message+="\n"

        return message
        


    # def format_links_info(self):
    #     message=""
    #     keep=['redirected', 'suspicious','malware','phishing','category']
    #     for i, data in enumerate(self.links):
    #         message+=f"Domain {i+1}\n{data['domain']}\n"
    #         for key, value in data.items():
    #             if key not in keep:
    #                 continue
    #             message+=f"{key}: {value}\n"
    #         message+="\n"

    #     return f"<table>{message}</table>"
        
    # def format_email_info(self):
    #     message=""
    #     keep=['disposable','leaked']
    #     content=self.checkEmailAddress()
    #     message+=f"Sender Email\n{content['sanitized_email'][1:-1]}\n"
    #     for key, value in content.items():
    #         if key not in keep:
    #             continue
    #         message+=f"{key}: {value}\n"
    #     message+="\n"

    #     return f"<table>{message}</table>"

    def __str__(self):
        return f"{self.sender}\n{self.subject}\n{self.body}"
    