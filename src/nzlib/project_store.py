import redis
import logging

class ProjectStore:
    
    KEY_PROJECT_SET = 'p:__[[main_db]] k:project_list'
    PROJECT_NAME_INVALID_CHAR = '`~!@#$%^&*()={[]};:\'"<>/?'
    
    def __init__(self, project_name:str, redis_param, create_project:bool=False):
        
        self._logger = logging.getLogger(type(self).__name__)
        
        self._logger.debug(f'<__init__> {project_name = } {create_project = }')
        
        self.__validate_project_name(project_name)
        self._project_name = project_name
        
        self._r_client = redis.StrictRedis(**redis_param)
        
        self._project_prefix = self.__get_project_prefix()
        
        if create_project:
            
            if self._r_client.sismember(self.KEY_PROJECT_SET, self._project_prefix):
                raise ValueError(f'Project "{project_name}" already exists. Remove the create_project flag if it is the project that you are trying to create.')
            else:
                self._r_client.sadd(self.KEY_PROJECT_SET, self._project_prefix)
        else:
            if not self._r_client.sismember(self.KEY_PROJECT_SET, self._project_prefix):
                raise ValueError(f'Project "{project_name}" does not exists. Set create_project flag=True if wish to create a project with the name.')
    
    
    # def hset(self, hname, hkey, kval)->int:
        
    #     name_key = f'{self.__get_project_prefix()} k:{hname}'
    #     return self._r_client.hset(name_key, hkey, kval)
    
    def __get_project_prefix(self):
        return f'p:{self._project_name}'
    
    def __validate_project_name(self, project_name:str):
        
        if any( (ch in self.PROJECT_NAME_INVALID_CHAR) for ch in project_name):
            raise ValueError(f'Project name cannot container any of the following character: {self.PROJECT_NAME_INVALID_CHAR}  Input project name: "{project_name}" ')
    
    
    def make_key(self, name: str):
        """Create key (index value) for an object in this project by
        prefix with project prefix and k prompt."""
        return f'{self.__get_project_prefix()} k:{name}'
    
    def delete(self, name:str):
        key = self.make_key(name)
        self._logger.info(f'Deleting object with key = "{key}"')
        return self._r_client.delete()
        
    def get_dictionary(self, dict_name:str):
        class ProjectStoreHash:
            
            def __init__(self, store:ProjectStore, dict_name:str):
                self._store = store
                self._dict_name = dict_name
                # self._r_client = store._r_client
                
                # The _index is the key for the whole hash in Redis
                self._index = store.make_key(dict_name)
                
            def set(self, key:str, val):
                return self._store._r_client.hset(self._index, key, val)
            
            def mset(self, dict):
                return self._store._r_client.hmset(self._index, dict)
            
            def get(self, key:str):
                return self._store._r_client.hget(self._index, key)
            
            def get_str(self, key:str, encoding:str='UTF-8'):
                obj = self.get(key)
                
                if obj:
                    return obj.decode(encoding = encoding)
                else:
                    return None
            
            def delete(self, key:str):
                return self._store._r_client.hdel(self._index, key)
            
            def exists(self, key:str):
                return self._store._r_client.hexists(self._index, key)
            
            def get_all(self):
                return self._store._r_client.hgetall(self._index)
            
            def get_all_str(self, encoding:str='UTF-8'):
                
                result = {}
                
                dict_all = self.get_all()
                
                for idx, val in dict_all.items():
                    result[idx.decode(encoding)] = val.decode(encoding)
                
                if result and len(result) > 0:
                    return result
                else:
                    return None
            
            def keys(self):
                return self._store._r_client.hkeys(self._index)
            
            def delete_all(self):
                self._store._r_client.delete(self._index)
            
        return ProjectStoreHash(self, dict_name)
    
    def get_set(self, set_name:str):
        """TODO. Implement the ability to store and access a set."""
        pass
    
    def keys(self):
        return self._r_client.keys(self.__get_project_prefix() + " k:*")

if __name__ == '__main__':
    # print('testing!')


    redis_param = {
        "host": "xxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx.databases.appdomain.cloud",
        "port": 32196,
        "db": 0,
        "password": "XXXXXXXXXXXXXXXXXXXXXXX",
        "username": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "ssl": True,
        "ssl_cert_reqs": "required",
        "ssl_ca_data": "-----BEGIN CERTIFICATE-----\nsdfasdfasdf\n-----END CERTIFICATE-----"
    }
        
    store = ProjectStore("redis_testing", redis_param, create_project=False)

    print(f'{store.keys() = }')
    
    dict = store.get_dictionary('TranslationDictionary')
    
    print(f'{dict = }')    
    
    # print(f'{dict.set("Key 1", "val 1123123") = }')
    
    print(f'{dict.get("Key 1") = }')
    
    print(f'{dict.getall() = }')
