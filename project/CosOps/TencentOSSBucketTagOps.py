from cosOps import TencentOSS
from typing import Any

class TencentOSSBucketTagOps(TencentOSS):

    def __init__(self,secret_id, secret_key, region, token=None, scheme='https'):
        super(TencentOSSBucketTagOps,self).__init__(secret_id, secret_key, region, token=token, scheme=scheme)

    @property
    def getBucketsTags(self):
        tagDicts = {}
        for bucket in self.getBuckets:
            # print(bucket['Name'])
            try:
                tagDicts[bucket['Name']] = \
                    self._client.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']['Tag']
            except Exception as _:
                pass

        return tagDicts

    @property
    def getNewCreatedBucketsTags(self):
        return {name: item
                for name,item in self.getBucketsTags.items()
                if name in self.newbkList}

    def setBucketsTags(self, bkList, tagList: Any):
        # set tags for bucket
        if isinstance(tagList,dict):
            tagList = [{'Key': key, 'Value': value} for key, value in tagList.items()]

        tagValueList = {
            'TagSet': {
                'Tag': tagList
            }
        }
        print(tagValueList)
        for bk in bkList:
            self._client.put_bucket_tagging(
                Bucket=f"{bk}-{self.APPID}",
                # 标签键不能以 项目、project、qcs: 开头
                Tagging=tagValueList)

    def deleteBucketsTags(self,bkList):
        for item in bkList:
            self._client.delete_bucket_tagging(item)


    def addBucketsTags(self,bkList,newTag):
        ori_bkList = bkList.copy()
        bkList = [f"{name}-{self.APPID}" for name in bkList]
        oldTagDicts={name:item
                     for name, item in self.getBucketsTags.items()
                     if name in bkList}
        for item in ori_bkList:
            newList=oldTagDicts.get(f"{item}-{self.APPID}",[])
            oldTagKeyList = [item['Key'] for item in newList]
            print(oldTagKeyList)
            newList.extend([{'Key': key, 'Value': value}
                            for key, value in newTag.items()
                            if key not in oldTagKeyList])
            print(newList)
            self.setBucketsTags([item],tagList=newList)

    def modifyBucketsTags(self,bkList,newTag):
        ori_bkList = bkList.copy()
        bkList = [f"{name}-{self.APPID}" for name in bkList]
        oldTagDicts={name:item
                     for name, item in self.getBucketsTags.items()
                     if name in bkList}
        for item in ori_bkList:
            newList=oldTagDicts.get(f"{item}-{self.APPID}",[])
            oldTagKeyList = [item['Key'] for item in newList]
            # print(oldTagKeyList)
            for k,v in newTag.items():
                if k in oldTagKeyList:
                    # print(oldTagKeyList.index(k))
                    newList[oldTagKeyList.index(k)]['Value'] = v
                else:
                    newList.append({'Key': k, 'Value': v})
            # print(newList)
            self.setBucketsTags([item],tagList=newList)


