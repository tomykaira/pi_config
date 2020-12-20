#!/usr/bin/env python

# Simplest Switchbot Command
# https://gist.github.com/mugifly/77e5ba2a2f1186bb7d494a90d4317695
# Thanks to https://gist.github.com/aerialist/163a5794e95ccd28dc023161324009ed

from __future__ import print_function
import binascii
import os.path
import pickle
import sys
import time

from bluepy.btle import Peripheral, BTLEDisconnectError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ** YOUR SPREAD SHEET ADDRESS **
SAMPLE_RANGE_NAME = 'Sheet1!B1:B1'

mac = ** YOUR MAC ADDRESS **
mode = 'press'

def query():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if len(values) > 0:
      return int(values[0][0])
    else:
      return None

def press():
    print('Connecting... %s' % mac)
    try:
        p = Peripheral(mac, 'random')
        hand_service = p.getServiceByUUID('cba20d00-224d-11e6-9fb8-0002a5d5c51b')
        hand = hand_service.getCharacteristics('cba20002-224d-11e6-9fb8-0002a5d5c51b')[0]
        
        if mode == 'on':
            print('On')
            hand.write(binascii.a2b_hex('570101'))
        elif mode == 'off':
            print('Off')
            hand.write(binascii.a2b_hex('570102'))
        elif mode == 'press':
            print('Press')
            hand.write(binascii.a2b_hex('570100'))
        
        p.disconnect()
    except BTLEDisconnectError:
        print("Failed to connect BLE, retry in 5 seconds")
        time.sleep(5)
        press()

def main():
    v = query()
    print("Initial value %d" % v)
    while True:
        new_v = query()
        if new_v > v:
            print("Value changes to %d" % new_v)
            press()
        v = new_v
        time.sleep(10)

if __name__ == '__main__':
    main()




