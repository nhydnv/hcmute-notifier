from datetime import datetime, timedelta
from fetch_messages import getGeneralMessages, getStudentMessages
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
import os

class Message:
  def __init__(self, id, subject, body, create_date):
    self.id = id
    self.subject = subject
    self.body = body
    try:
      self.create_date = datetime.fromisoformat(create_date)
    except ValueError: self.create_date = None

  def is_new(self):
    now = datetime.now()
    # A message is considered new if it was posted in the last 24 hours
    return (self.create_date <= now and self.create_date > now - timedelta(days=1))
  
  def send(self, to_addr):
    from_addr = os.environ['SENDER']
    msg = EmailMessage()
    msg['Subject'] = 'subject'
    msg['FROM'] = from_addr
    msg['TO'] = to_addr
    msg.set_content('content')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
      server.login(
        from_addr,
        os.environ['SENDER_APP_PASSWORD'],
      )
      server.send_message(msg, from_addr=from_addr, to_addrs=to_addr)

  def __str__(self):
    return f"Message ID: {self.id}\nSubject: {self.subject}\n{self.body}"

class GeneralMessage(Message):
  def __init__(self, msg):
    super().__init__(msg['MaTin'], msg['TieuDe'], msg['NoiDung'], msg['CreateDate'])

class StudentMessage(Message):
  def __init__(self, msg):
    super().__init__(msg['MessageID'], msg['MessageSubject'], msg['MessageBody'], msg['CreationDate'])

m = GeneralMessage(getGeneralMessages()[0])
m.send('mungkeumeomeo@gmail.com')