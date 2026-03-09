from dotenv import load_dotenv
import requests
import os

# Return access token for HCMUTE APIs for this student
def getAccessToken():
  # Load username, password, API key
  load_dotenv()

  auth_url = "https://portalapi.hcmute.edu.vn/api/authenticate/authpsc"
  headers = {
    'Apikey': os.environ['API_KEY'],
    'Clientid': 'ute',
    'Origin': 'https://online.hcmute.edu.vn'
  }

  payload = {
    'username': os.environ['HCMUTE_USERNAME'],
    'password': os.environ['HCMUTE_PASSWORD'],
    'type': 0,
  }

  cookies = { 'cookiesession1': '678ADA5B168B762849B8A8B0C43FDBA8' }

  r = requests.post(auth_url, headers=headers, json=payload, cookies=cookies)
  return r.json()['Token']