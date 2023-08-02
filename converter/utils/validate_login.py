import requests 


URL = r'http://app:8000/login'


def login(data_login, url = URL ) : 
        
    """ validate login into url"""
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


    response = requests.post(url, headers=headers, json=data_login, timeout=5)

    return response


