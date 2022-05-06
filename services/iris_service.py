from subprocess import call
from services.api_service import ApiService
from urllib import response

class IrisService:

    BASE_URL = "http://13.127.100.81:8000/api/v1"

    @staticmethod
    def get_drone_uuid(machine_id, serial_id):
        url = f'{IrisService.BASE_URL}/avionics_box/{machine_id}/{serial_id}/uuid'
        print(url)
        api_response = ApiService.get(url, caller = 'init')
        return api_response

    @staticmethod
    def get_credentials(uuid):
        url = f"{IrisService.BASE_URL}/avionics_box/{uuid}/credentials"
        api_response = ApiService.get(url, caller='init')
        return api_response

    @staticmethod
    def get_manufacturer_public_key():
        url = f"{IrisService.BASE_URL}/manufacturer/pubkey"
        api_response = ApiService.get(url, caller='init')      
        print(api_response)
        return api_response.json()["manufacturer's public key"]

    @staticmethod
    def update_registration_status(uuid):
        url = f"{IrisService.BASE_URL}/avionics_box/{uuid}/acknowledge_registration"
        api_response = ApiService.put(url)
        return api_response

    @staticmethod
    def get_latest_enabled_firmware(drone_id):
        url = f"{IrisService.BASE_URL}/drone/{drone_id}/firmware/master/latest"
        api_response = ApiService.get(url, caller='secure_firmware_update')
        return api_response.json()["latest_enabled_firmware"]  

    # @staticmethod
    # def get_manufacturer_public_key():
    #     url = f"{IrisService.BASE_URL}/manufacturer/pubkey"
    #     api_response = ApiService.get(url)
    #     manufacturer_key_file_path = 'manufacturer.public.pem'
    #     with open(manufacturer_key_file_path, 'wb') as file:
    #         file.write(api_response.content)
    #     return manufacturer_key_file_path      

    