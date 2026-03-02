from dotenv import load_dotenv
from authorization import getAccessToken
import requests
import os

general_messages_url = "https://portalapi.hcmute.edu.vn/api/student/GetAllThongBaoChung"
student_messages_url = "https://portalapi.hcmute.edu.vn/api/student/GetMessagesByReceiverID"

load_dotenv()

# Set up request header
api_key = os.environ['API_KEY']
api_token = getAccessToken()
headers = {
  'Apikey': f'{api_key}',
  'Clientid': 'ute',
  'Authorization': f'Bearer {api_token}',
  'Origin': 'https://online.hcmute.edu.vn',
}

# Return a JSON array of all general messages
def getGeneralMessages():
  return requests.get(general_messages_url, headers=headers).json()

# Return a JSON array of all student messages
def getStudentMessages():
  return requests.get(student_messages_url, headers=headers).json()