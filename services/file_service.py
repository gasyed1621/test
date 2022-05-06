import json
from os import path

class FileService:
    AWS_certs_path = '/home/root/mount/AWS_IoT_certs/'

    @staticmethod
    def check_credentials_existence():
        iot_certificate_exists = path.exists('/home/root/mount/AWS_IoT_certs/device.pem.crt')
        iot_private_key_exists = path.exists('/home/root/mount/AWS_IoT_certs/private.pem.key')
        iot_public_key_exists = path.exists('/home/root/mount/AWS_IoT_certs/public.pem.key')
        drone_private_key_exists = path.exists('/home/root/mount/AWS_IoT_certs/drone.private.key')
        drone_public_key_exists = path.exists('/home/root/mount/AWS_IoT_certs/drone.public.key')
        manufacturer_pub_key_exists = path.exists('/home/root/mount/AWS_IoT_certs/manufacturer.public.key')

        if iot_certificate_exists and iot_private_key_exists and iot_public_key_exists and drone_private_key_exists and drone_public_key_exists and manufacturer_pub_key_exists:
            return True
        else:
            return False

    @staticmethod
    def update_param_file(path_to_file, data):
        with open(path_to_file, "w") as json_file:
            json.dump(data, json_file, indent=4)
    
    @staticmethod
    def create_file(name, content):        
        with open(f'{FileService.AWS_certs_path}+{name}', 'w+') as credential_file:
            credential_file.write(content)