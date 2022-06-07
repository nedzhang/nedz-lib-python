import s3fs
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import logging

logger = logging.getLogger(__file__)

def write_patable_to_cos(endpoint_url:str, cos_credential: dict, bucket: str, 
                      object_key: str, ptable: pa.Table)->None:
      
    s3 = s3fs.S3FileSystem(anon=False, 
              key=cos_credential['cos_hmac_keys']['access_key_id'], 
              secret=cos_credential['cos_hmac_keys']['secret_access_key'],
              client_kwargs={'endpoint_url': endpoint_url})

    logger.info(f'<write_patable_to_cos> sending {object_key}')
    
    pq.write_table(ptable, 
                    f's3://{bucket}/{object_key}',
                    filesystem=s3) #, use_dictionary=True, compression='snappy')


def write_csv_to_cos(endpoint_url:str, cos_credential: dict, bucket: str, 
                      object_key: str, csv_dataframe: pd.DataFrame, index=True)->None:
      
    s3 = s3fs.S3FileSystem(anon=False, 
              key=cos_credential['cos_hmac_keys']['access_key_id'], 
              secret=cos_credential['cos_hmac_keys']['secret_access_key'],
              client_kwargs={'endpoint_url': endpoint_url})

    logger.info(f'<write_csv_to_cos> sending {object_key}')
    
    with s3.open(f's3://{bucket}/{object_key}', mode='w') as f:
        csv_dataframe.to_csv(f, index=index)
    
    

def open_cos_file(endpoint_url:str, cos_credential:dict, bucket:str, 
                      object_key:str, mode:str='rb'):
      
    s3 = s3fs.S3FileSystem(anon=False, 
              key=cos_credential['cos_hmac_keys']['access_key_id'], 
              secret=cos_credential['cos_hmac_keys']['secret_access_key'],
              client_kwargs={'endpoint_url': endpoint_url})

    logger.info(f'<open_cos_file> opening {object_key}')
    
    return s3.open(f's3://{bucket}/{object_key}', mode=mode)