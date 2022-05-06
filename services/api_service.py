from subprocess import call
import requests
from services.exception_service import CustomException

class ApiService:

    @staticmethod
    def get(request_url, caller):
        '''
            Makes a GET API request.

            Parameters:
            request_url (string): API request URL.
        
            Returns:
            Response object or None.
        '''
       
        response = requests.get(url=request_url)
        if caller == 'secure_firmware_update':
            if response.status_code == 200:
                return response
            else:
                raise CustomException(f"Status Code : {response.status_code}")
        elif caller == 'init':
            if response.status_code == 201 or response.status_code == 403 or response.status_code == 200 or response.status_code == 400:
                return response
            else:
                print("Some Error while getting credentials")
                raise CustomException(f"Status Code : {response.status_code}")
                
    @staticmethod
    def put(request_url):
        response = requests.put(url=request_url)
        if response.status_code == 204 or response.status_code == 400:
            return response
        else:
            print(response.status_code)
            print("Some Error while acknowledging")
            raise CustomException(f"Status Code : {response.status_code}")


    @staticmethod
    def get_file(url, target_file):
        retry_count = None
        while True:
            try:
                retry_count = retry_count + 1
                with open(target_file, "wb") as file:
                    with requests.get(url, stream=True, timeout=10) as r:
                        for chunk in r.iter_content(chunk_size=1024):
                            file.write(chunk)
            except Exception as e:
                if r.status_code != 200:
                    if retry_count == 3:
                        raise Exception("File download retry count exceeded")
                else:
                    return


