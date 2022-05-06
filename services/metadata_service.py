import json
import os

class MetadataService:
    def __init__(self, data) -> None:
        '''
            Description

            Parameters:
            name (type): description.
        
            Returns:
            name (type): description.
        ''' 
        self.version = data["version"]
        self.ap_version = data["ap_version"]
        self.ap_checksum = data["ap_checksum"]
        self.cc_version = data["cc_version"]
        self.cc_checksum = data["cc_checksum"]

    @classmethod
    def load_from_file(cls, path_to_file):
        '''
            Description

            Parameters:
            name (type): description.
        
            Returns:
            name (type): description.
        ''' 
        with open(path_to_file, 'r') as metadata_file:
            data = json.loads(metadata_file.read())
        return cls(data)

    @staticmethod
    def delete(path_to_file):
        '''
            Description

            Parameters:
            name (type): description.
        
            Returns:
            name (type): description.
        ''' 
        os.remove(path_to_file)
    
    def update_metadata(self, new_metadata):
        '''
            Description

            Parameters:
            name (type): description.
        
            Returns:
            name (type): description.
        ''' 
        self.version = new_metadata.version
        self.ap_version = new_metadata.ap_version
        self.ap_checksum = new_metadata.ap_checksum
        self.cc_version = new_metadata.cc_version
        self.cc_checksum = new_metadata.cc_checksum
        
    def write_to_metadata(self, path_to_file):
        '''
            Description

            Parameters:
            name (type): description.
        
            Returns:
            name (type): description.
        ''' 
        MetadataService.delete(path_to_file)

        with open(path_to_file, 'w+') as current_metadata_file:
            current_metadata_file.write(json.dumps(self))
        current_metadata_file.close()
        



        

         
        
