from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from pprint import pprint


class minioOps:
    def __init__(self,cfg,bucket='zach'):
        SERVER_URL = cfg.SERVER_URL
        AK = cfg.AK
        SK = cfg.SK
        SSL_ENABLE = cfg.SSL_ENABLE
        SERVER_LOC = cfg.SERVER_LOC
        self.minioClient = Minio(SERVER_URL,
                            access_key=AK,
                            secret_key=SK,
                            secure=SSL_ENABLE)
        self.bucket=bucket
        self.location = SERVER_LOC

    def upload(self,object_name,file_path,metadata,content_type='application/text'):
        # Make a bucket with the make_bucket API call.
        try:
               self.minioClient.make_bucket(self.bucket, location=self.location)
        except BucketAlreadyOwnedByYou as _:
               pass
        except BucketAlreadyExists as _:
               pass
        except ResponseError as _:
               return 500

        try:
               # print(content_type,metadata)
               self.minioClient.fput_object(self.bucket, object_name,file_path,content_type,metadata)
        except ResponseError as err:
               print(err)
               return 500
        return 200

    def listAllobjects(self,prefix=""):
        return self.minioClient.list_objects_v2(self.bucket, prefix,recursive=True)

    def listObjectsInfo(self,prefix=''):
        for obj in self.listAllobjects():
            output_format = f'''
BucketName: {obj.bucket_name}
FileName: {obj.object_name.encode('utf-8')}
LastModifyTime: {obj.last_modified}
Etag: {obj.etag}
Size: {obj.size}
MetaData: {self.statObjectInfo(obj.object_name)}
            '''
            print(output_format,end="")

    def getObjectInfo(self,objname):
        obj = self.minioClient.get_object(self.bucket,objname)
        return obj.read()

    def statObjectInfo(self,objname):
        obj = self.minioClient.stat_object(self.bucket,objname)
        return obj.metadata

    def getAllMetadataFromCurrentPath(self,dirname=""):
        metadataDict={}
        for obj in self.listAllobjects(dirname):
            metadataDict[obj.object_name.encode('utf-8')] = self.statObjectInfo(obj.object_name)
        pprint(metadataDict)
        return metadataDict

    def getObjectFile(self,filename,savepath="."):
        try:
            self.objInfo=self.minioClient.fget_object(self.bucket, filename, savepath)
        except ResponseError as err:
            print(err)
        return self

    @property
    def getDownloadObjectInfo(self):
        import time
        from os.path import basename
        output_format = \
            f'''BucketName: {self.objInfo.bucket_name}
FileName: {self.objInfo.object_name.encode('utf-8')}
LastModifyTime: {time.strftime("%Y-%m-%d %X",self.objInfo.last_modified)}
Etag: {self.objInfo.etag}
Size: {self.objInfo.size}
Content-type: {self.objInfo.content_type}
MetaData: {self.objInfo.metadata}'''
        with open(basename(self.objInfo.object_name)+'.info', 'w') as f:
            f.write(output_format)
        # print(output_format, end="")
        return 200

    def getAllObjectFileFromCurrentPath(self,dirname="",savepath="."):
        for obj in self.listAllobjects(dirname):
            self.getObjectFile(obj.object_name.encode('utf-8'),savepath)
        return 200


# if __name__ ==  '__main__':
#     from sys import argv
#     if argv[1].lower() == 'prd':
#         from config import ProductionConfig
#         cfg = ProductionConfig()
#     elif argv[1].lower() == 'dev':
#         from config import DevelopmentConfig
#         cfg = DevelopmentConfig()
#     else:
#         from config import TestingConfig
#         cfg = TestingConfig()
#
#     SERVER_URL = cfg.SERVER_URL
#     AK = cfg.AK
#     SK = cfg.SK
#     SSL_ENABLE = cfg.SSL_ENABLE
#     SERVER_LOC = cfg.SERVER_LOC
#
#     zachbucket = minioOps()
#     # metadata = {'x-amz-meta-testing': 'value'}
#     # zachbucket.upload('aaa/shadw.png','D:\moban5001\img\image\shadow.png',metadata=metadata,content_type='application/x-png')
#     # zachbucket.getAllMetadataFromCurrentPath('')
#
#     zachbucket.getObjectFile('aaa/shadw.png',".\\shadw.png").getDownloadObjectInfo
#
#     # zachbucket.getObjectInfo('ds6')
#     # zachbucket.statObjectInfo('server2.py')