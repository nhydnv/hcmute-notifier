from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
import logging
import os

class Message:
  def __init__(self, id, subject, body, create_date, sender):
    self.id = id
    self.subject = subject
    self.body = body
    self.sender = sender
    self.create_date = create_date

  def is_new(self):
    now = datetime.now()
    # A message is considered new if it was posted in the last 24 hours
    return (self.create_date <= now and self.create_date > now - timedelta(days=1))
  
  def send(self, recipients):
    from_addr = os.environ['SENDER']
    msg = EmailMessage()
    msg['Subject'] = f'[HCMUTE Portal] New Message: {self.subject}'
    msg['FROM'] = from_addr
    msg['TO'] = ", ".join(recipients)

    header = f'<p><strong>From:</strong> {self.sender}</p>' \
             f'<p><strong>Date:</strong> {self.create_date.strftime('%d/%m/%y')}</p>' \
             f'<p><strong>Subject:</strong> {self.subject}</p>'
    
    self.body = f'{header}<hr>{self.body}'

    # Plain text fallback
    plain_text = BeautifulSoup(self.body, 'html.parser').get_text()
    msg.set_content(plain_text)

    # HTML content
    msg.add_alternative(self.body, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
      server.login(
        from_addr,
        os.environ['SENDER_APP_PASSWORD'],
      )
      for to_addr in recipients:
        logging.info(f"Sending message '{self.subject}' to {to_addr}")
      try:
        server.send_message(msg, from_addr=from_addr, to_addrs=recipients)
      except Exception as e:
        logging.error(f"Failed to send '{self.subject}': {e}")
      logging.info(f"Successfully sent '{self.subject}'")

  def __str__(self):
    return f"Message ID: {self.id}\nSubject: {self.subject}\n{self.body}"

class GeneralMessage(Message):
  def __init__(self, msg):
    try:
      create_date = datetime.fromisoformat(msg['CreateDate'])
      super().__init__(msg['MaTin'], msg['TieuDe'], msg['NoiDung'], create_date, msg['StaffName'])
    except ValueError: self.create_date = None

class StudentMessage(Message):
  def __init__(self, msg):
    try:
      create_date = datetime.strptime(msg['CreationDate'], "%d/%m/%Y")
      super().__init__(msg['MessageID'], msg['MessageSubject'], msg['MessageBody'], create_date, msg['SenderName'])
    except ValueError: self.create_date = None