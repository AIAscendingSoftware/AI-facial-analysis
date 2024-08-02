
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

class APIs:
    def __init__(self):
        self.half_url="http://192.168.29.222:8086/api/proCommunication" #server:192.168.1.29:8083,, java local:192.168.29.222:8086

    def get_details(self,id, max_retries=3, backoff_factor=0.3, timeout=10):
        base_url = f"{self.half_url}/details/getAlldetails/{id}"
        print(base_url)
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

    def post_one_video_result(self,data, max_retries=3, backoff_factor=0.3, timeout=30):

        url = f"{self.half_url}/details/postDetails"

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
                    response = session.post(url, json=data, timeout=timeout)
                    response.raise_for_status()
                    return "POST post_one_video_result successful", "Response:", response.json()
                except requests.RequestException as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(backoff_factor * (2 ** attempt))
        except requests.RequestException as e:
            print(f"An error occurred after {max_retries} attempts: {e}")
            print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
            print(f"Response content: {e.response.content if e.response else 'N/A'}")
            return "POST post_one_video_result failed", "Status code:", e.response.status_code if e.response else 'N/A', "Response:", e.response.text if e.response else 'N/A'
        finally:
            session.close()

    def post_final_data(self,data, max_retries=3, backoff_factor=0.3, timeout=10):
        url = f"{self.half_url}/overAllDetails/post"
        print(url, data)
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
                    response = session.post(url, json=data, timeout=timeout)
                    response.raise_for_status()
                    print("POST final request successful")
                    print("Response:", response.json())

                except requests.RequestException as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(backoff_factor * (2 ** attempt))
        except requests.RequestException as e:
            print(f"An error occurred after {max_retries} attempts: {e}")
            print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
            print(f"Response content: {e.response.content if e.response else 'N/A'}")
        finally:
            session.close()




# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# import time


# def get_details(id, max_retries=3, backoff_factor=0.3, timeout=10):
#     base_url = f"http://192.168.29.223:8080/api/proCommunication/details/getAlldetails/{id}"
    
#     # Create a session object
#     session = requests.Session()
    
#     # Configure retry strategy
#     retries = Retry(total=max_retries,
#                     backoff_factor=backoff_factor,
#                     status_forcelist=[500, 502, 503, 504])
    
#     # Mount the adapter to the session
#     session.mount('http://', HTTPAdapter(max_retries=retries))
    
#     try:
#         for attempt in range(max_retries):
#             try:
#                 response = session.get(base_url, timeout=timeout)
#                 response.raise_for_status()
#                 return response.json()
#             except requests.RequestException as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt == max_retries - 1:
#                     raise
#                 time.sleep(backoff_factor * (2 ** attempt))
#     except requests.RequestException as e:
#         print(f"An error occurred after {max_retries} attempts: {e}")
#         print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
#         print(f"Response content: {e.response.content if e.response else 'N/A'}")
#         return None
#     finally:
#         session.close()


# # def post_one_video_result(data):
# #     url = "http://192.168.29.223:8080/api/proCommunication/postDetails"

# #     response = requests.post(url, json=data)
# #     if response.status_code == 200:
# #         return "POST post_one_video_result successful","Response:", response.json()

# #     else:
# #         return "POST post_one_video_result failed","Status code:", response.status_code, "Response:", response.text
# def post_one_video_result(data, max_retries=3, backoff_factor=0.3, timeout=10):
#     print('post_one_video_result:', data)
#     url = "http://192.168.29.223:8080/api/proCommunication/details/postDetails"
    
#     # Create a session object
#     session = requests.Session()

    
#     # Configure retry strategy
#     retries = Retry(total=max_retries,
#                     backoff_factor=backoff_factor,
#                     status_forcelist=[500, 502, 503, 504])
    
#     # Mount the adapter to the session
#     session.mount('http://', HTTPAdapter(max_retries=retries))
    
#     try:
#         for attempt in range(max_retries):
#             try:
#                 response = session.post(url, json=data, timeout=timeout)
#                 response.raise_for_status()
#                 return "POST post_one_video_result successful", "Response:", response.json()
#             except requests.RequestException as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt == max_retries - 1:
#                     raise
#                 time.sleep(backoff_factor * (2 ** attempt))
#     except requests.RequestException as e:
#         print(f"An error occurred after {max_retries} attempts: {e}")
#         print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
#         print(f"Response content: {e.response.content if e.response else 'N/A'}")
#         return "POST post_one_video_result failed", "Status code:", e.response.status_code if e.response else 'N/A', "Response:", e.response.text if e.response else 'N/A'
#     finally:
#         session.close()

# def post_final_data(data, max_retries=3, backoff_factor=0.3, timeout=10):
#     url = "http://192.168.29.223:8080/api/proCommunication/overAllDetails/post"
    
#     # Create a session object
#     session = requests.Session()
    
#     # Configure retry strategy
#     retries = Retry(total=max_retries,
#                     backoff_factor=backoff_factor,
#                     status_forcelist=[500, 502, 503, 504])
    
#     # Mount the adapter to the session
#     session.mount('http://', HTTPAdapter(max_retries=retries))
    
#     try:
#         for attempt in range(max_retries):
#             try:
#                 response = session.post(url, json=data, timeout=timeout)
#                 response.raise_for_status()
#                 print("POST final request successful")
#                 print("Response:", response.json())
      
#             except requests.RequestException as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt == max_retries - 1:
#                     raise
#                 time.sleep(backoff_factor * (2 ** attempt))
#     except requests.RequestException as e:
#         print(f"An error occurred after {max_retries} attempts: {e}")
#         print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
#         print(f"Response content: {e.response.content if e.response else 'N/A'}")
#     finally:
#         session.close()