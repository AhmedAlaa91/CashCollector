from django.http import HttpResponse
import requests
def checkUserStatusApi():
  api_url = f'http://127.0.0.1:8000/all-users-status/'


  response = requests.get(api_url)


  if response.status_code == 406:
    
    return (response.status_code)
    
  else:
    
    return (response.status_code)