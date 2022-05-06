from email.mime import image
import json
import subprocess

with open('config.json', 'r') as config_file:
    CONFIG = json.loads(config_file.read())

class DockerService:
    def login_to_dockerhub():
        '''
            Description

            Parameters:
            name (type): description.

            Returns:
            name (type): description.
        ''' 
        login_try_count = 0     
        invalid_credentials = b'incorrect username or password'
        while True:           
            login_try_count = login_try_count + 1
            proc = subprocess.Popen(
                [f"docker", f"login", f"--username", f"{CONFIG['USERNAME']}", f"--password", f"{CONFIG['PASSWORD']}"], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            (stdout, stderr) = proc.communicate(timeout=12)
            if proc.returncode!=0:
                if invalid_credentials in stderr:
                    raise Exception("Invalid Credentials")
                if login_try_count == 3:
                    raise Exception("Retry count exceeded")
            else:
                return


    @staticmethod
    def pull_docker_image(image_tag):
        '''
            Description

            Parameters:
            name (type): description.

            Returns:
            name (tuple): (Success, Image checksum).
        '''
        docker_pull_command = [f"docker", f"pull", f"{CONFIG['ORGANIZATION']}/{CONFIG['REPO']}:{image_tag}"]
        subprocess.check_output(docker_pull_command)
        image_checksum = DockerService.get_image_checksum(CONFIG['ORGANIZATION'], CONFIG['REPO'], image_tag)
        return image_checksum

    @staticmethod
    def get_image_checksum(image_tag):
        docker_checksum_command = f"docker inspect --format='{{{{.RepoDigests}}}}' {CONFIG['ORGANIZATION']}/{CONFIG['REPO']}:{image_tag}"
        process_checksum = subprocess.Popen(docker_checksum_command, stdout=subprocess.PIPE, shell=True) 
        # process_checksum -> 
        checksum = process_checksum.communicate()[0].decode().rstrip().split(":")[1][:-1]
        return checksum

    @staticmethod
    def delete_docker_image(image_tag):
        '''
            Description

            Parameters:
            name (type): description.

            Returns:
            name (tuple): (Success, Image checksum).
        '''
        delete_docker_image_command = f"docker rmi -f {CONFIG['ORGANIZATION']}/{CONFIG['REPO']}:{image_tag}"
        subprocess.call(delete_docker_image_command, shell=True)

    @staticmethod
    def create_docker_container(image_tag):
        '''
            Description

            Parameters:
            name (type): description.

            Returns:
            name (type): description.
        '''
        docker_container_create_command = f"docker container create -it --privileged --name cc-{image_tag} --net host --ipc=host " \
            f"-v /home/root/mount/NPNT:/work-dir/NPNT " \
            f"-v /home/root/mount/lastlog:/work-dir/lastlog " \
            f"-v /home/root/mount/AWS_IoT_certs:/work-dir/util/iot_source/certs " \
            f"-v /home/root/mount/aws_iot.config:/work-dir/util/iot_source/aws_iot.config " \
            f"-v /home/root/mount1:/work-dir/mount1/ " \
            f"-v /home/root/mount/logs:/work-dir/logs " \
            f"-v /home/root/mount/param:/work-dir/param/ " \
            f"-v /lib:/lib " \
            f"-v /usr/lib:/usr/lib " \
            f"-v /sbin:/sbin {CONFIG['ORGANIZATION']}/{CONFIG['REPO']}:{image_tag}"
        subprocess.check_output(docker_container_create_command)

    @staticmethod
    def start_docker_container(image_tag):
        '''
            Description

            Parameters:
            name (type): description.

            Returns:
            name (type): description.
        '''
        start_docker_container_command = f"docker start -ai cc-{image_tag}"
        subprocess.call(start_docker_container_command, shell=True)

    
    @staticmethod
    def delete_docker_container(image_tag):
        '''
            Description

            Parameters:
            name (type): description.

            Returns:
            name (type): description.
        '''
        delete_docker_container_command = f"docker rm cc-{image_tag}"
        subprocess.call(delete_docker_container_command, shell=True)
    


