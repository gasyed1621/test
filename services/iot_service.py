# In-built packages
import time, uuid
import json
import urllib
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from AWSIoTPythonSDK.exception.AWSIoTExceptions import connectError


class IOT:
    awsiotcore_config       = None
    awsiotcore_client       = None
    connected_to_internet   = False
    connected_to_aws        = False
    mqtt_responses          = {}
    stop_all_threads        = False
    stop_task_execution     = False

    #local internet checking facility 
    def check_internet():
        host="http://google.com"
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False

    #initialize with connection to IOT core
    def __init__(self):
        self.core_connection()

    #Connect to AWS IOT core MQTT client and configure as per config file
    def core_connection(self):
        with open('/home/root/mount/aws_iot.config') as cf:
            self.awsiotcore_config = json.load(cf)
        self.awsiotcore_client = AWSIoTPyMQTT.AWSIoTMQTTClient(clientID=self.awsiotcore_config["CLIENT_ID"])
        self.awsiotcore_client.configureEndpoint(hostName=self.awsiotcore_config["ENDPOINT"], portNumber=8883)
        self.awsiotcore_client.configureCredentials(CAFilePath=self.awsiotcore_config["PATH_TO_ROOT"], KeyPath=self.awsiotcore_config["PATH_TO_KEY"], CertificatePath=self.awsiotcore_config["PATH_TO_CERT"])
    
    # Try connecting, return SUCCESS if connected
    def connect(self):
        CONN_STATUS = {"SUCCESS":0, "NO_INTERNET":1}
        try:
            self.awsiotcore_client.connect()
            self.connected_to_aws = True
            return CONN_STATUS["SUCCESS"]
        except Exception as e:
            if e.strerror=='getaddrinfo failed' and not IOT.check_internet():  
                return CONN_STATUS["NO_INTERNET"]

    def get_url(self, to_download, drone_id):
        # retry if failes to get url'
        connection = self.connect()
        if connection == 1:
            return "No Internet"
        self.subscribe(topic=f'response/{drone_id}/urls')
        time.sleep(2)
        print("\n(MQTT) Publishing firmware request message.")  # ---------------step 1
        firmware_publish_response = self.publish(type="FWR", data={'pending_firmware': to_download},
                                                publish_topic='test/request', response_topic=f'response/{drone_id}/urls')
        
        url = firmware_publish_response['presigned_url'][to_download]

        return url

    # Publish a message to AWS MQTT on provided TOPIC & CHANNEL
    def publish(self, type, data, publish_topic, response_topic):
        print(f"\nPublishing for the data : {data}")
        message_id = str(uuid.uuid1())
        message = {
            'DRONE_ID'  : data["DRONE_ID"],
            'CLIENT_ID' : self.awsiotcore_config["CLIENT_ID"], 
            'MSG_ID'    : message_id, 
            'MSG_TYPE'  : type, 
            'MSG_DATA'  : data, 
            'RES_TOPIC' : response_topic, 
            'EDKEY'     : self.awsiotcore_config["EDKEY"],
            #'EDKEY'     : data["edkey"]
        }
        if type == 'DEC':
            message['EDKEY']=data["edkey"] 
        response = ""
        while(True):
            try:
                self.mqtt_responses[message_id] = None
                self.awsiotcore_client.publish(topic=publish_topic, payload=json.dumps(message), QoS=1)
                while(self.mqtt_responses[message_id] == None):
                    continue
                response = self.mqtt_responses[message_id]
                break
            except Exception as e:
                print(f"\n[ IOT.publish ] Exception caught : {e}")
        return response

    def subscribe(self, topic):
        def subscriber_callback(client, userdata, message):
            print(f"\n [ IOT.subscriber_callback ] New message received from {message.topic}")
            # print(f'New message from {message.topic} topic:\n{message.payload}\n')
            res = json.loads(message.payload.decode('utf-8'))
            if res['MSG_ID'] in self.mqtt_responses:
                self.mqtt_responses[res['MSG_ID']] =  res
        
        try:
            self.awsiotcore_client.subscribe(topic=topic, QoS=1, callback=subscriber_callback)
        except Exception as e:
            print(f"\n[ IOT.subscribe ] Exception caught : {e}")
    
    def disconnect(self):
        try:
            self.awsiotcore_client.disconnect()
        except Exception as e:
            print(f"\n[ IOT.disconnect ] Exception caught : {e}")
            pass
