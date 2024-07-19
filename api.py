


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

def post_data(data):
    # API endpoint URL
    url = 'http://192.168.29.223:8080/api/proCommunication/postDetails'

    # Making the POST request
    response = requests.post(url, json=data)

    # Checking the response
    if response.status_code == 200:
        return 'POST request successful.'
    else:
        print(response.text) 
        return f'POST request failed with status code: {response.status_code}'


def get_details(id, max_retries=3, backoff_factor=0.3, timeout=10):
    base_url = f"http://192.168.29.223:8080/api/proCommunication/getdetails/{id}"
    
    # Create a session object
    session = requests.Session()
    
    # Configure retry strategy
    retries = Retry(total=max_retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=[500, 502, 503, 504])
    
    # Mount the adapter to the session
    session.mount('http://', HTTPAdapter(max_retries=retries))
    
    try:
        for attempt in range(max_retries):
            try:
                response = session.get(base_url, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(backoff_factor * (2 ** attempt))
    except requests.RequestException as e:
        print(f"An error occurred after {max_retries} attempts: {e}")
        print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
        print(f"Response content: {e.response.content if e.response else 'N/A'}")
        return None
    finally:
        session.close()

def post_final_data(data):
    url = "http://192.168.29.223:8080/api/proCommunication/postAllDetailsScore"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("POST finall request successful")
        print("Response:", response.json())
    else:
        print("POST final request failed")
        print("Status code:", response.status_code)
    print("Response:", response.text)
