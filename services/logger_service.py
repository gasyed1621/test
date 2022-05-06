from asyncio.log import logger
import logging
import os

from datetime import datetime
class Logger:
    logger = None
    def __init__(self):       
           
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Log file name
        Bl_logFileName = 'test_log'
        # if not os.path.exists('/home/root/mount/logs/bl'):
        #     os.makedirs('/home/root/mount/logs/bl')
        # log_files = os.listdir('/home/root/mount/logs/bl')

        # Bl_logfileCount = 0
        # if len(log_files) != 0:
        #     for i in range(len(log_files)):
        #         if "_bootloader_log_" in log_files[i]:
        #             try:
        #                 splitfilename = log_files[i].split('_')
        #                 if int(splitfilename[0]) > Bl_logfileCount:
        #                     Bl_logfileCount = int(splitfilename[0])
        #             except:
        #                 pass
        #     Bl_logfileCount+=1
        # Bl_logFileName = "{}_bootloader_log__%H_%M_%d_%m_%Y".format(Bl_logfileCount)

        logging.basicConfig(
            filename=datetime.now().strftime(Bl_logFileName),
            level=logging.INFO, 
            format= '%(asctime)s.%(msecs)03d,%(filename)-12s,%(levelname)-8s,%(message)s',
            datefmt='%H:%M:%S')

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        LogFormat = logging.Formatter('%(asctime)s.%(msecs)03d,%(filename)-12s,%(levelname)-8s,%(message)s')
        stream_handler.setFormatter(LogFormat)
        logging.getLogger('').addHandler(stream_handler)
