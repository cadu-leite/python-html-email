#!/usr/bin/env python3

import smtplib
import sys
import re
import os
import csv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid


class EmailMsg():
    def __init__(self):

        self.host = None  # smtp host
        self.port = None  # smtp host port
        self.password = None  # smpt password (account used to send)
        self.from_sender = None  # The email account used to send

        self.to_recipient = None  # list of receivers
        self.mailtolistfile = None  # list of receivers

        self.subject = None  # the email subject
        self.content_html = None  # user raw HTML content
        self.content_text = None  # user raw text content

        # for internal use
        self._images_cids = None  # images x CIds (images and respectives Content ID)
        self._content_html = None  # the raw html content
        self._content_html_cleaned = None  # html content parse result
        self._msg = None  # the instance of MIMEMultipart
        self._content_html_file = None  # html content file path
        # self._mailtolist = None  # recipients list
        self._mailtolistfile = None

        self._msg = MIMEMultipart()  # initiate the instance of MIMEMultipart - crap

    @property
    def content_html(self):
        # to read property self.content_html
        return self._content_html

    @content_html.setter
    def content_html(self, value):
        '''
        kept the HML content of email message.
        This setter make a copy to internal :attr:`_content_html` property
        then call :meth:`set_images_cids()` to parse the html content

        returns:
            sets :attr:`_content_html` as defined by the user

        '''
        self._content_html = value
        self.set_images_cids()

    @property
    def content_html_file(self):
        """file PATH pointing to html content file.

        Returns:
            str: a file path copy from internal  :attr:`_content_html_file` property
        """
        return self._content_html_file

    @content_html_file.setter
    def content_html_file(self, path):
        '''
        kept the raw HTML file path
        returns:
            sets :attr:`content_html` with the content of the file pointed by :attr:`_content_html_file`
        '''
        self._content_html_file = path
        if path:
            with open(path, 'r') as f:
                self.content_html = f.read()

    @property
    def mailtolistfile(self):
        """file PATH pointing to html content file.

        Returns:
            str: a file path copy from internal  :attr:`_content_html_file` property
        """
        return self._mailtolistfile

    @mailtolistfile.setter
    def mailtolistfile(self, path):
        '''
        get list from recipients file
        '''
        rcps = []
        if path:
            self._mailtolistfile = path
            with open(self._mailtolistfile, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
                for row in csv_reader:
                    rcps.append(row[0])
            self.to_recipient = rcps

    def set_images_cids(self):
        '''Parse the html content (:attr:`content_html` property)
        to get Images paths
        AND set a content Id  (CIds)
        AND (that's bad) swap the image tag source attribute  (<img src='uri'>) with the CIDs (<img src='cid:<id>'>)

        Returns:
            :attr:`_images_cids` = The tuple (CID, Image)
            :attr:`_content_html_cleaned` = the parsed html with CIds

        TODO: break it in smaller pieces.
        '''

        if self.content_html is not None:
            match = re.findall(r'src="(.*?)"', self.content_html)
            if len(match) > 0:
                self._images_cids = [(count, value) for count, value in enumerate(set(match))]
            else:
                self._images_cids = []
        else:
            self._images_cids = None

        if self._images_cids is not None:
            self._content_html_cleaned = self.content_html
            for count, value in self._images_cids:
                self._content_html_cleaned = self._content_html_cleaned.replace(value, f'cid:{count}')

    def add_image_attachments(self):
        '''
        add image attachments to the MIMEMultipart instance

        returns:
            :_attr:`_msg` instance attached with images found on HTML content
        '''
        if self._images_cids:
            for count, value in self._images_cids:
                if self.content_html_file:
                    value = os.path.abspath(os.path.join(self.content_html_file, f'../{value}'))
                with open(value, 'rb') as img:
                    image = MIMEImage(img.read())
                    image.add_header('Content-ID', f'<{count}>')
                self._msg.attach(image)

    def add_text_attachments(self):
        '''
        add TEXT attachments to the MIMEMultipart instance

        returns:
            :_attr:`_msg` instance attached with texts (html and plain text)
        '''
        try:
            part = MIMEText(self.content_text, 'plain')  # add content
        except AttributeError:
            sys.stdout.write('Plain text content seems to be empty\n')
            part = MIMEText('', 'plain')
        finally:
            self._msg.attach(part)

        try:
            part = MIMEText(self._content_html_cleaned, 'html')  # add content
        except AttributeError:
            sys.stdout.write('Html text content seems to be empty\n')
            part = MIMEText('', 'html')
        finally:
            self._msg.attach(part)

    def send(self):

        self.add_text_attachments()
        self.add_image_attachments()

        self._msg['Subject'] = self.subject
        self._msg['From'] = self.from_sender
        self.smtp()

    def smtp(self):
        # Send the message via local SMTP server.
        smtp_server = smtplib.SMTP_SSL(self.host, self.port)  # usando Google
        smtp_server.ehlo()
        smtp_server.login(self.from_sender, self.password)

        for rec in self.to_recipient:
            #  smtp_server.send_message(msg)
            smtp_server.sendmail(self.from_sender, rec, self._msg.as_string())
            # msg['To'] = rec
            # smtp_server.send_message(msg)
        smtp_server.quit()
