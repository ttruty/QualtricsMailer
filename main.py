#!/usr/bin/env python

import requests
import json
from time import gmtime, strftime
import sys
import logging
import sys


"""
A simple python script to automate qualtrics survey distributions.
Tutorial at https://medium.com/kaianalytics/automating-surveys-with-python-qualtrics-api-and-windows-task-scheduler-4bffc58726d7
and https://api.qualtrics.com/docs/code-to-send-sms-or-email-1
"""


# logging info

# logs http response to track success and errors
# can comment out if logging is not needed
# or can set location to cloud service like dropbox, google drive, or box to check survey distributions remotely
root = logging.getLogger()
root.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('qualtrics-mailer.log') # can change location of log
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
root.addHandler(fh)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
root.addHandler(handler)

# remember to close the handlers
for handler in root.handlers:
    handler.close()
    root.removeFilter(handler)
# end logging
	
# qualtrics API object IDs
mailingListId = "ML_###############" # NEED TO SET
messageId = 'MS_###############'     # NEED TO SET
libraryId = 'UR_###############'     # NEED TO SET
surveyId = 'SV_###############'      # NEED TO SET

def email(apiToken, dataCenter):

    headers = {
        "x-api-token": apiToken,
        "Content-Type": "application/json"
    }

    header = {}
	#NEED TO SET MAILER OPTIONS
    header['fromEmail'] = "noreply@qualtrics.com"
    header['fromName'] = "The CART team at [YOUR SITE]" # NEED TO SET
    header['replyToEmail'] = "YOUR_EMAIL@site.edu"      # NEED TO SET
    header['subject'] = "Weekly Health Update Form"     # CAN CHANGE

    surveyLink = {}
    surveyLink['surveyId'] = surveyId
    surveyLink['type'] = "Individual"

    message = {}
    message["libraryId"] = libraryId
    message["messageId"] = messageId

    recipients = {}
    recipients["mailingListId"] = mailingListId

    data = {}
    data['header'] = header
    data['surveyLink'] = surveyLink
    data['recipients'] = recipients
    data['sendDate'] = strftime('%Y-%m-%dT%H:%M:%SZ', gmtime())
    data['message'] = message

    # print(data) #debug 

    url = 'https://{0}.qualtrics.com/API/v3/distributions'.format(dataCenter)
    response = requests.post(url, json=data, headers=headers)
    # print(response.text) #debug


def main():
    try:
		# NEED TO SET
        apiToken = '#########API TOKEN ###########' # hard coding API token for ease, but can set as env variable
        dataCenter = '####### DATA CENTER ########' # will be the same across sites. 
    except KeyError:
        print("set environment variables APIKEY and DATACENTER")
        sys.exit(2)

    # print("Sending email") #debug
    email(apiToken, dataCenter)

if __name__ == "__main__":
    main()