import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cam.v20190116 import cam_client, models
import string,random

class CAMOps:
    def __init__(self,AK,SK,endpoint="cam.tencentcloudapi.com",project='zach'):
        self.cred = credential.Credential(AK,SK)
        self.ep = endpoint
        self.proj = project

        httpProfile = HttpProfile()
        httpProfile.endpoint = self.ep

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self._client = cam_client.CamClient(self.cred, "", clientProfile)

class PolicyOps(CAMOps):

    def getPolicyId(self,PolicyName="QcloudCOSReadOnlyAccess"):
        try:

            req = models.ListPoliciesRequest()
            params = {
                "Keyword": PolicyName
            }
            req.from_json_string(json.dumps(params))

            resp = self._client.ListPolicies(req)
            return resp.List[0].PolicyId

        except TencentCloudSDKException as err:
            print(err)

    def bindUserPolicy(self,PolicyID, UserID):
        try:
            req = models.AttachUserPolicyRequest()
            params = {
                "PolicyId": PolicyID,
                "AttachUin": int(UserID)
            }
            req.from_json_string(json.dumps(params))

            resp = self._client.AttachUserPolicy(req)
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)

class UserTokenOperator(CAMOps):
    # def __init__(self,AK,SK,endpoint="cam.tencentcloudapi.com",project='zach'):
    #     super(UserTokenOperator, self).__init__(AK,SK, endpoint=endpoint, project=project)

    def generateRandName(self,len=8):
        letters = string.ascii_lowercase
        return self.proj+'-'+''.join(random.choice(letters) for _ in range(len))

    def generateNewToken(self):
        uname = self.generateRandName()
        try:

            req = models.AddUserRequest()
            params = {
                "Name": uname,
                "Remark": self.proj,
                "ConsoleLogin": 0,
                "UseApi": 1
            }
            req.from_json_string(json.dumps(params))

            resp = self._client.AddUser(req)
            print(resp)

        except TencentCloudSDKException as err:
            print(err)



user1 = PolicyOps("AK", "SK")
userid = "10001"
readcosonlyid = user1.getPolicyId(PolicyName="QcloudCOSReadOnlyAccess")
print(readcosonlyid)
user1.bindUserPolicy(readcosonlyid,userid)