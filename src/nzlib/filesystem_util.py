import inspect
import logging
import pathlib
import s3fs
from typing import Union

logger = logging.getLogger(__name__)

def make_dir(directory:Union[str, pathlib.Path])->None:
    
    if isinstance(directory, pathlib.Path):
        tgt_dir = directory
    else:
        tgt_dir = pathlib.Path(directory)
        
    # ensure the output direction exists
    tgt_dir.mkdir(parents=True, exist_ok=True)

    return tgt_dir



def get_cfp(real: bool = False) -> str:
    """Return caller's current file path.

    Args:
        real: if True, returns full path, otherwise relative path
            (default: {False})
    """
    frame = inspect.stack()[1]
    p = frame[0].f_code.co_filename
    if real:
        return os.path.realpath(p)
    return p


def resolve_path(path:str, ref_dir:pathlib.Path=None)->pathlib.Path:
    """
    Resvolce a path.
    
    Arg:
        path: the string value of a relative or absolute path. 
        ref_dir: the reference directory to resolve relative path. If 
        ref_dir is not provide. The current working directory is 
        used as reference (not caller's file path). 
    """
    
    if ref_dir:
        ref_dir_path = pathlib.Path(ref_dir)
    else:
        ref_dir_path = pathlib.Path('.')
        
    if path:
        path_path = pathlib.Path(path)
        
        if path_path.is_absolute():
            result_path = path_path
        else:
            result_path = ref_dir_path / path
    else:
        result_path = ref_dir_path
    
    return result_path.resolve()


def open_file(store_root: Union[pathlib.Path, s3fs.S3FileSystem], path:str, key: str, mode:str='rb'):
    """Open a file from location filesystem or S3.
    Args:
        store_root: the root of the storage. Can be a path or S3Filesystem
        path: path before the key (includ / at the end if it is a directory)
        key: name/key of the object
        mode: opening mode. Default to rb
    """

    obj_path = f"{path or ''}{key or ''}"

    if store_root is None:
        return open(obj_path, mode=mode)
    elif isinstance(store_root, pathlib.Path):
        full_path = store_root / obj_path
        return open(full_path, mode=mode)
    elif isinstance(store_root, s3fs.S3FileSystem ):
        return store_root.open(obj_path, mode=mode)