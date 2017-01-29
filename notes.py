#!/usr/bin/env python
# -*- coding: utf-8 -*-
import email
from email.header import decode_header
import imaplib
import html2text
import sys
import os
import shutil
import click


@click.command()
@click.option('--imap', help='Exampl Gmail: imap.gmail.com')
@click.option('--user', help='Example: my@gmail.com')
@click.option('--password', help='Example: 123456')
def get_notes(imap, user, password):
    # Connect
    mail = imaplib.IMAP4_SSL(imap)
    mail.login(user, password)
    # Get data
    mail.list()
    mail.select("Notes")
    result, data = mail.search(None, "ALL")
    ids = data[0]
    # Ids is a space separated string
    folder = 'notes/'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(os.path.dirname(folder))
    # List of IDs
    id_list = ids.split()
    # List alls messages
    for key, item in enumerate(id_list):
        # Get message
        result, data = mail.fetch(item, "(RFC822)")
        raw_email = data[0][1]
        # Parse data
        msg = email.message_from_bytes(raw_email)
        # Get subject
        try:
            subject_html = decode_header(msg['Subject'])[0][0].decode('utf-8')
        except Exception:
            subject_html = decode_header(msg['Subject'])[0][0]
        # Get body
        try:
            body_html = msg.get_payload(decode=True).decode('utf-8')
        except Exception:
            body_html = msg.get_payload(decode=True)
        # Get markdown
        if body_html:
            # Get text
            subject_md = html2text.html2text(str(subject_html)).strip()
            body_md = html2text.html2text(str(body_html)).strip()
            # Save
            filename = folder + (subject_md.replace('/', '-')) + '.md'
            new_file = open(filename, 'a')
            new_file.write(body_md)
            new_file.close()
            # Progress
            progress(key, len(id_list), subject_md)
    # Print information
    print('\nFinish! 100%')


def progress(count, total, status=''):
    '''
    Print progress bar
    '''
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


if __name__ == '__main__':
    get_notes()
