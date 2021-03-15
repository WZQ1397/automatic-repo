from cosOps import TencentOSS


class TencentOSSFileTagOps(TencentOSS):

    def __init__(self, secret_id, secret_key, region, token=None, scheme='https'):
        super(TencentOSSFileTagOps, self).__init__(secret_id, secret_key, region, token=token, scheme=scheme)

    def getFileList(self, bucket, path='/'):
        if not self.checkBucketsExists(bucket):
            return f"Bucket: {bucket} is not exists!"

        if path != '' and path.endswith('/'):
            path = path[:-1]
        len_path = len(path)
        func = self._client.list_objects
        file_list = func(Bucket=bucket, Prefix=path)['Contents'] \
            if len_path else func(Bucket=bucket)['Contents']
        return self.showFiles(file_list, len_path)

    def showFiles(self, file_list, len_path):
        files = []
        directories = []
        for blob in file_list:
            remote_file = blob['Key'][len_path + 1:] if len_path else blob['Key']
            pos_slash = remote_file.find('/')
            if pos_slash == -1 and remote_file != '':  # files
                files.append(remote_file)
            else:  # directory
                dir_name = remote_file[:pos_slash]
                if dir_name == '':
                    continue
                if dir_name not in directories:
                    directories.append(remote_file[:pos_slash])
        return ({"dirs": directories}, {"files": files})

    def getFileMetaTags(self, bucket, file):
        tagDicts = {}
        response = self._client.head_object(Bucket=bucket, Key=file)
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