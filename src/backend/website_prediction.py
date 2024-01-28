import argparse
import urlextract
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


    

def main():
    class model:
        def __init__(self, model_path="src/backend/model"):
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
            keep = ['redirected', 'suspicious', 'malware', 'phishing', 'category']
            html_message = "<table border='1'>"  # Start of the table

            for i, data in enumerate(self.links):
                row = f"Domain {i+1}: {data['domain']}"  # Domain row
                for key, value in data.items():
                    if key not in keep:
                        continue
                    row += f"{key}: {value}\n"  # Data rows

                html_message += f"<tr><td>{row}</td></tr>"  # Add the completed row to the table

            html_message += "</table>"  # End of the table

            return html_message


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
        

    print('here')
    # Create the parser
    parser = argparse.ArgumentParser(description='predict email')

    # Add arguments
    parser.add_argument('--body', type=str, help='body of the email in question')
    parser.add_argument('--email', type=str, help='email to send the results to')

    # Parse the arguments
    args = parser.parse_args()

    smtpServer = 'smtp.gmail.com'
    user = 'phishnetcombatant@gmail.com'
    password = 'tfen yldy bojq fujw'
    # Use the arguments
    if args.body and args.email:
        e=Email(user, 'test', args.body, {'From': args.email})
        confidence_percentage = e.prediction['score'] * 100
        e.reply(
        f"Phishnet Combatant is {confidence_percentage:.1f}% confident that this is a {'safe' if e.get_prediction()[0]['label'] == 'SAVE EMAIL' else 'potentially dangerous'} email.\n\n"+
        f"{len(e.links)} links were found in this email.\n"+
        e.format_links_info()
                )   


if __name__ == "__main__":
    main()
