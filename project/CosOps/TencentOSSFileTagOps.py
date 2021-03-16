from cosOps import TencentOSS


class TencentOSSFileTagOps(TencentOSS):

    def __init__(self, secret_id, secret_key, region, token=None, scheme='https'):
        super(TencentOSSFileTagOps, self).__init__(secret_id, secret_key, region, token=token, scheme=scheme)

    def getFileList(self, bucket, path='/',max_items=1000):
        if not self.checkBucketsExists(bucket):
            return f"Bucket: {bucket} is not exists!"

        len_path = len(path)
        if len_path>=2 and path.startswith('/'):
            path = path[1:]
        print(path)
        func = self._client.list_objects
        # print(func(Bucket=bucket, Prefix=path, MaxKeys=max_items)['Contents'])
        file_list = func(Bucket=bucket, Prefix=path,MaxKeys=max_items)['Contents']
        # print(file_list)
        return self.showFiles(file_list, len_path)

    def showFiles(self, file_list, len_path):
        files = []
        directories = []
        for blob in file_list:
            remote_file = blob['Key'][len_path-1:] if len_path else blob['Key']
            pos_slash = remote_file[-1] == '/'
            if pos_slash is False and remote_file != '':  # files
                files.append(remote_file)
            else:  # directory
                dir_name = remote_file
                if dir_name == '':
                    continue
                if dir_name not in directories:
                    directories.append(remote_file)
        return ({"emptydirs": directories}, {"files": files})

    def getFileMetaTags(self, bucket, file):
        from qcloud_cos import CosServiceError
        tagDicts = {}
        try:
            response = self._client.head_object(Bucket=bucket, Key=file)
        except CosServiceError:
            return tagDicts
        for k, v in response.items():
            if k.startswith('x-cos-meta'):
                tagDicts[k] = v
        return tagDicts


class TencentOSSFileTransferOps(TencentOSS):
    _Bucket: str

    def __init__(self, secret_id, secret_key, region, bucket, token=None, scheme='https'):
        super(TencentOSSFileTransferOps, self).__init__(secret_id, secret_key, region, token=token, scheme=scheme)
        self._Bucket = bucket

    def uploadFile(self, fileList, metaData={}, storagePath='/', maxSpeed='1048576'):
        from os.path import basename
        for file in fileList:
            filename = basename(file)
            response = self._client.upload_file(
                Bucket=self._Bucket,
                Key=storagePath + filename,
                LocalFilePath=file,
                PartSize=5,
                MAXThread=5,
                EnableMD5=True,
                Metadata=metaData,
                TrafficLimit=maxSpeed
            )
            print(response["ETag"])
            

    def downloadFile(self, fileList, storagePath='/', maxSpeed='1048576'):
        from os.path import basename
        for file in fileList:
            filename = basename(file)
            self._client.download_file(
                Bucket=self._Bucket,
                Key=storagePath + filename,
                PartSize=5,
                MAXThread=5,
                TrafficLimit=maxSpeed,
                DestFilePath=storagePath
            )