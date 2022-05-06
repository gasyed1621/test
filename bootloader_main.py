from os import path
from globals import Globals
from services.file_service import FileService
#from init.init_main import DroneRegistration
import git

if __name__ == "__main__":
    # Run production init
    # git fetch to find secure firmware.py updates
    # running secure firmware update.py
    # secure boot of docker container or CC 
    # running exixsting docker container

    # Production init 
    # Checks
    Globals.initialize_param()
    drone_uuid = Globals.get_param_val('UUID')
    first_boot = Globals.get_param_val('FIRST_BOOT')

    # Production Init
    if first_boot:
        print("This is first boot {}".format(first_boot))
        #register_drone = DroneRegistration()
       # register_drone.start_registration(drone_uuid=drone_uuid)
        print("One time regitration of drone is completed.")

    else:
        if drone_uuid is None:
            #register_drone = DroneRegistration()
            #register_drone.start_registration(drone_uuid=drone_uuid)
            print("Drone UUID received and set")
        elif not FileService.check_credentials_existence():
            #register_drone = DroneRegistration()
            #register_drone.start_registration(drone_uuid=drone_uuid)
            print("Drone credentials received and saved")

    #git fetch to find secure firmware.py updates
    #running secure firmware update.py
    # pip install gitpython


    git_dir = "D:\REPOS\Github\test"
    g = git.cmd.Git(git_dir)
    g.pull()

    # if not drone_uuid and not FileService.check_credentials_existence():
    #     print("Not Present")
    # # 
    # pass