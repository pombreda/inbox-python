#!/usr/bin/python

import os
import time
from inbox import APIClient
from inbox.util import generate_id

APP_ID = '[YOUR_APP_ID]'
APP_SECRET = '[YOUR_APP_SECRET]'
ACCESS_TOKEN = '[YOUR_ACCESS_TOKEN]'
inbox = APIClient(APP_ID, APP_SECRET, ACCESS_TOKEN)

ns = inbox.namespaces[0]

subject = generate_id()
# Create a new draft
draft = ns.drafts.create()
draft.to = [{'name': 'Inbox PythonSDK', 'email': 'inboxtestempty@gmail.com'}]
draft.subject = subject
draft.body = ""

for filename in filter(lambda x: not os.path.isdir(x), os.listdir(".")):
    f = open(filename, 'r')
    attachment = ns.files.create()
    attachment.filename = filename
    attachment.stream = f
    attachment.save()
    draft.attach(attachment)

draft.send()

th = ns.threads.where({'tag': 'sent', 'subject': subject}).first()
while not th:
    time.sleep(0.5)
    th = ns.threads.where({'tag': 'sent', 'subject': subject}).first()

print th.messages[0].attachments[0].download()
