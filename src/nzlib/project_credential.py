import logging
import os
import pathlib
from typing import Dict
import json

from nzlib import logging_util
from nzlib import filesystem_util


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#Python3
class ProjectCredential(metaclass=Singleton):
    """
    A singleton class that provides project secret
    """

    def __init__(self, dir_to_search:str):
        self._logger = logging.getLogger(type(self).__name__)
        
        self._secret = self.__read_secret_files(dir_to_search)
        
        super().__init__()
        
        self._logger.info(f'<__init__> finished __init__ with {dir_to_search = }')
    
    
    @property
    def credential(self):
        return self._secret
    
    
    def __read_secret_files(self, dir_to_search:str)->Dict:
        
        secret = {}
        
        SECRET_FILE_EXT = ('.secret.json', '.secret.yaml')
        
        # secret_dir = filesystem_util.resolve_path(dir_to_search)
        # print(f'{secret_dir = }')
        
        for dirpath, dirnames, filenames in os.walk(dir_to_search, ):
            dir_path = pathlib.Path(dirpath)
            
            for f in filenames:
                if (f.endswith(SECRET_FILE_EXT)):
                    secret_file = dir_path / f
                    self._logger.info(f'<__read_secret_files> loading secret from {f}')
                    new_secret = self.__read_file(secret_file)
                    
                    secret = dict(secret, **new_secret)
                    # print(f'{secret = }')
            
            break # stop at the first level (not recursive)
        
        return secret
        
    def __read_file(self, file_path:pathlib.Path):
        if (file_path.suffix == '.json'):
            with open(file_path, 'r') as f:
                return json.load(f)
        

if __name__ == "__main__":
    
    logging_util.config_logging(logging.DEBUG)
    
    a = ProjectCredential('./')
    b = ProjectCredential()
    c = ProjectCredential()
    
    
    print(f'{c._secret = }')