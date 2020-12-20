# pi config

My raspberry pi configs

## switchbot

Automate switch bot control by Google Spreadsheet.

See Google document to set up python client. You must have credentials.json and token.pickle in your running directory.
Create spreadsheet that has a number in B1 column. Write arbitrary number and count up when you want to trigger switch bot.
Use systemd to automate running the script.

https://developers.google.com/sheets/api/quickstart/python
