# In-built packages
from calendar import c
import json
import logging
import os
from services.api_service import ApiService
# Services
from services.docker_service import DockerService
from services.iris_service import IrisService
from services.iot_service import IOT
from services.logger_service import Logger
from services.metadata_service import MetadataService
from pymavlink import mavutil
from services.s3_service import S3Service
from services.security_service import SecurityService

from ardupilot_update import ArdupilotUpdate
from companion_computer_update import CompanionComputerUpdate

if __name__== "__main__":
    logger = Logger().logger
    try:
        with open('config.json', 'r') as config_file:
            CONFIG = json.loads(config_file.read())
        with open(CONFIG["RFM_INFO_PATH"], "r") as rfm_info_file:
            rfm_info = json.loads(rfm_info_file.read())
            logger.info(f"Drone ID : {rfm_info['RPAS_ID']} | Drone Type : {rfm_info['RPAS_MODEL_ID']}")
        current_firmware_metadata = MetadataService.load_from_file(path_to_file = CONFIG["CURRENT_FIRMWARE_METADATA_PATH"])
        print(f'{current_firmware_metadata.cc_version}')
        latest_enabled_firmware = IrisService.get_latest_enabled_firmware(drone_id = rfm_info['RPAS_ID'])
        latest_firmware_metadata = MetadataService(latest_enabled_firmware["metadata"])
        latest_firmware_metadata = IrisService.get_latest_enabled_firmware(drone_id = rfm_info['RPAS_ID'])
        print(latest_firmware_metadata["cc_version"])
        latest_firmware_signature = latest_enabled_firmware["signature"]
        if not os.path.exists(CONFIG["MANUFACTURER_PUBLIC_KEY_PATH"]):
            manufacturer_public_key_path = IrisService.get_manufacturer_public_key
            CONFIG["MANUFACTURER_PUBLIC_KEY_PATH"] = manufacturer_public_key_path
            with open('config.json', 'w+') as config_file:
                config_file.write(json.dumps(CONFIG, indent=4))
            config_file.close()

        verified_update_source = SecurityService.verify_digital_signature(
            data = json.dumps(latest_firmware_metadata, separators=(',', ':')),
            signature = latest_firmware_signature,
            path_to_pubkey = CONFIG["MANUFACTURER_PUBLIC_KEY_PATH"]
        )
        print("Latest FWU update : {}".format(latest_firmware_metadata["version"]))
        update_required = (current_firmware_metadata.version != latest_firmware_metadata["version"])
        if verified_update_source and update_required:
            if update_required:
                ap_update_required = (current_firmware_metadata.ap_version != latest_firmware_metadata["ap_version"])
                cc_update_required = (current_firmware_metadata.cc_version != latest_firmware_metadata["cc_version"])
                if cc_update_required: 
                    DockerService.login_to_dockerhub(dockerhub_username = CONFIG["DOCKER"]["USERNAME"], dockerhub_password = CONFIG["DOCKER"]["PASSWORD"])
                    image_checksum = DockerService.pull_docker_image(organization = CONFIG["ORGANIZATION"], repo = CONFIG["REPO"], cc_version = latest_firmware_metadata["cc_version"])
                    checksum_mismatch = (latest_firmware_metadata["cc_checksum"] != image_checksum)
                    if checksum_mismatch:
                        CompanionComputerUpdate.rollback(cc_version = latest_firmware_metadata["cc_version"])
                        raise Exception()              
                if ap_update_required:
                    try:
                        apj_url = IOT().get_url(filename_to_download = [f"ap-{latest_firmware_metadata['ap_version']}.apj"], drone_id = rfm_info['RPAS_ID'])
                        ApiService.get_file(url=apj_url, target_file=f"{CONFIG['ARDUPILOT_FIRMWARE_FOLDER_PATH']}/ap-{latest_firmware_metadata['ap_version']}.apj")
                        ap_file_checksum = SecurityService.get_checksum()
                        checksum_mismatch = (latest_firmware_metadata["ap_checksum"] != ap_file_checksum)
                        if checksum_mismatch:
                            raise Exception()
                    except Exception as e:
                        if cc_update_required:
                            CompanionComputerUpdate.rollback(latest_cc_version=latest_firmware_metadata["cc_version"])
                            ArdupilotUpdate.delete_apj_file(path_to_file = f"{CONFIG['ARDUPILOT_FIRMWARE_FOLDER_PATH']}/ap-{latest_firmware_metadata['ap_version']}.apj")
                            raise Exception()
                            ArdupilotUpdate.rollback(latest_ap_version = latest_firmware_metadata["ap_version"])
                            
                if cc_update_required:    
                    CompanionComputerUpdate.start(latest_cc_version = latest_firmware_metadata["cc_version"], curr_cc_version = current_firmware_metadata["cc_version"])
                if ap_update_required:
                    ArdupilotUpdate.start(latest_ap_version = latest_firmware_metadata["ap_version"])
                    # Rollback CC
                current_firmware_metadata.update_metadata(latest_firmware_metadata)
                current_firmware_metadata.write_to_metadata(path_to_file = CONFIG["CURRENT_FIRMWARE_METADATA_PATH"])
                # delete metadata
            
    except Exception as e:
        trace = f'{e.__class__.__name__} : '
        if e.__class__.__name__ == "CustomException":
            trace = f'{e.__class__.__name__} ' + f"({str(e)})" + " : "
        traceback = e.__traceback__
        while traceback is not None:
            trace += f'[{traceback.tb_frame.f_code.co_filename.split("/")[-1]}, {traceback.tb_frame.f_code.co_name}, Line {traceback.tb_lineno}] > '
            traceback = traceback.tb_next
        trace = trace[:-3]
        logger.error(trace)
        
    DockerService.start_docker_container(current_firmware_metadata.cc_version)

