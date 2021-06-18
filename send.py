#!/usr/bin/python3

import smtplib
import ssl
import traceback
from email.message import EmailMessage
import csv

csv_name = input("Enter path to CSV: ")

with open(csv_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        title = row[0]
        last_name = row[1]
        org = row[2]
        email = row[3]

        body = (
            """
            %s %s,
            Thanks for signing up for our mailing list.
            We're happy your organization, %s, has joined us.

            Cheers,
            Daniel Limanowski
            """
            % (title, last_name, org)
        )

        msg = EmailMessage()
        msg['Subject'] = ("%s %s - mailing list" % (title, last_name))
        msg['From'] = "daniel@b1tst0rm.net"
        msg['To'] = email
        msg.set_content(body)

        context = ssl.create_default_context()

        try:
            # Do NOT use STMP_SSL, it fails negotiating SSL versions.
            # Instead use the starttls command to force encryption.
            server = smtplib.SMTP('smtp-relay.gmail.com', 587)
            server.set_debuglevel(1)
            server.starttls(context=context)
            server.send_message(msg)
            server.quit()
            print('Email sent!')
        except Exception:
            traceback.print_exc()
