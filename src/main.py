from message import Message
from fetch_messages import getGeneralMessages, getStudentMessages
from message import GeneralMessage, StudentMessage
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

logging.basicConfig(
  filename=Path(__file__).parent.parent / 'logs' / "hcmute_notifier.log",
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_messages(messages, message_class, recipients):
  total = 0
  for raw_msg in messages:
    msg = message_class(raw_msg)
    if not msg.is_new():
        break
    msg.send(recipients)
    total += 1
  return total

def main():
  logging.info("Script started")
  load_dotenv()
  recipients = os.environ['RECIPIENTS'].split(',')
  total_general = process_messages(getGeneralMessages(), GeneralMessage, recipients)
  total_student = process_messages(getStudentMessages(), StudentMessage, recipients)
  logging.info(f"Sent {sum([total_general, total_student])} emails")
  logging.info("Script ended")

if __name__ == '__main__':
  main()