import json

#from src.globals.ga_logging import GALogging
from sqlitedict import SqliteDict

class Globals:
    class ParamType:
        PARAM = 0
        MISSION_PARAM = 1
    ''' application global varibales'''
    SITL = False #True if the connection is SITL, else false
    GA_IMX7_FILE = None

    # parmeters related
    PARAM_FILE_1 = 'param/param.json'
    PARAM_FILE_2 = 'param/mission_param.json'
    MISSION_PARAM_FILE = SqliteDict("param/mission_param.sqlite")
    PARAM_FILE = SqliteDict("param/param.sqlite")
    MISSION_PARAMETER = dict()
    PARAMETER = dict()
    PARAMETER_KEYS = None
    MISSION_PARAMETER_KEYS = None
    import threading
    __param_set_lock = threading.Lock()
    __mission_param_set_lock = threading.Lock()

    @staticmethod
    def initialize_param():
        # with open(Globals.PARAM_FILE_1) as f:
        #     Globals.PARAMETER = json.load(f)
        # Globals.PARAMETER_KEYS = Globals.PARAMETER.keys()

        Globals.PARAMETER_KEYS = [key[0] for key in Globals.PARAM_FILE.items()]
        for key, val in Globals.PARAM_FILE.items():
            Globals.PARAMETER[key] = val
            print('PARAMETER, %s, %s' % (key, str(Globals.PARAMETER[key]['VAL'])))

        # with open(Globals.PARAM_FILE_2) as f:
        #     Globals.MISSION_PARAMETER = json.load(f)
        # Globals.MISSION_PARAMETER_KEYS = Globals.MISSION_PARAMETER.keys()

        Globals.MISSION_PARAMETER_KEYS = [key[0] for key in Globals.MISSION_PARAM_FILE.items()]
        for key, val in Globals.MISSION_PARAM_FILE.items():
            Globals.MISSION_PARAMETER[key] = val
            print('MISSION_PARAMETER, %s, %s' % (key, str(Globals.MISSION_PARAMETER[key])))

    @staticmethod
    def set_param(param_name, val, param_type = ParamType.PARAM):
        if param_type is Globals.ParamType.PARAM:
            if Globals.update_param(param_name, val, param_type):
                print('PARAMETER, %s, %s' % (param_name, Globals.PARAMETER[param_name]['VAL']))
                return True
            return False
        elif param_type is Globals.ParamType.MISSION_PARAM:
            if Globals.update_param(param_name, val, param_type):
                print('PARAMETER, %s, %s' % (param_name, Globals.MISSION_PARAMETER[param_name]['VAL']))
                return True
            return False

    @staticmethod
    def get_param_val(param_name, param_type = ParamType.PARAM):
        if param_type is Globals.ParamType.PARAM:
            if param_name in Globals.PARAMETER_KEYS:
                return Globals.PARAMETER[param_name]['VAL']
            else:
                return None
        elif param_type is Globals.ParamType.MISSION_PARAM:
            if param_name in Globals.MISSION_PARAMETER_KEYS:
                return Globals.MISSION_PARAMETER[param_name]['VAL']
            else:
                return None

    @staticmethod
    def get_param_id(param_name, param_type = ParamType.PARAM):
        if param_type is Globals.ParamType.PARAM:
            if param_name in Globals.PARAMETER_KEYS:
                return Globals.PARAMETER[param_name]['ID']
            else:
                return None
        elif param_type is Globals.ParamType.MISSION_PARAM:
            if param_name in Globals.MISSION_PARAMETER_KEYS:
                return Globals.MISSION_PARAMETER[param_name]['ID']
            else:
                return None

    @staticmethod
    def update_param(param_name, val, param_type = ParamType.PARAM):
        if param_type is Globals.ParamType.PARAM:
            with Globals.__param_set_lock:
                if param_name in Globals.PARAMETER_KEYS:
                    if 'MIN' in Globals.PARAMETER[param_name] and 'MAX' in Globals.PARAMETER[param_name]:
                        if Globals.PARAMETER[param_name]['MIN'] <= val <= Globals.PARAMETER[param_name]['MAX']:
                            Globals.PARAMETER[param_name]['VAL'] = val
                            return True
                    else:
                        Globals.PARAMETER[param_name]['VAL'] = val
                        return True
            return False
        elif param_type is Globals.ParamType.MISSION_PARAM:
            with Globals.__mission_param_set_lock:
                if param_name in Globals.MISSION_PARAMETER_KEYS:
                    if 'MIN' in Globals.MISSION_PARAMETER[param_name] and 'MAX' in Globals.MISSION_PARAMETER[param_name]:
                        if Globals.MISSION_PARAMETER[param_name]['MIN'] <= val <= Globals.MISSION_PARAMETER[param_name]['MAX']:
                            Globals.MISSION_PARAMETER[param_name]['VAL'] = val
                            return True
                    else:
                        Globals.MISSION_PARAMETER[param_name]['VAL'] = val
                        return True
            return False

    @staticmethod
    def add_mission_param(param_name, index, val):
       with Globals.__mission_param_set_lock:
            Globals.MISSION_PARAMETER[param_name] = {}
            Globals.MISSION_PARAMETER[param_name]['INDEX'] = index
            Globals.MISSION_PARAMETER[param_name]['VAL'] = val
            Globals.MISSION_PARAMETER_KEYS = [key for key in Globals.MISSION_PARAMETER]

    @staticmethod
    def delete_mission_param(param_name):
        with Globals.__mission_param_set_lock:
            Globals.MISSION_PARAMETER.pop(param_name)
            Globals.MISSION_PARAM_FILE.pop(param_name)

    @staticmethod
    def update_param_file():
        for key, val in Globals.PARAM_FILE.items():
            Globals.PARAM_FILE[key] = Globals.PARAMETER[key]
        Globals.PARAM_FILE.commit()

        # for key in Globals.PARAMETER:
        #     Globals.PARAM_FILE[key] = Globals.PARAMETER[key]
        # Globals.PARAM_FILE.commit()

        # with open(Globals.PARAM_FILE, 'w') as f:
        #     json.dump(Globals.PARAMETER, f, indent=4)

        Globals.update_mission_param_file()

    @staticmethod
    def update_mission_param_file():
        # with open(Globals.MISSION_PARAM_FILE, 'w') as f:
        #     json.dump(Globals.MISSION_PARAMETER, f, indent=4)

        for key in Globals.MISSION_PARAMETER:
            Globals.MISSION_PARAM_FILE[key] = Globals.MISSION_PARAMETER[key]
        Globals.MISSION_PARAM_FILE.commit()

        # for key, val in Globals.MISSION_PARAM_FILE.items():
        #     Globals.MISSION_PARAM_FILE[key] = Globals.MISSION_PARAMETER[key]
        # Globals.MISSION_PARAM_FILE.commit()


