from minioOps import minioOps
# from videoHandler import videoHandler
import time
from os.path import basename


class timeResolver:

    @staticmethod
    def get_current_date() -> str:
        return time.strftime("%Y-%m-%d", time.localtime())

if __name__ ==  '__main__':
    from sys import argv
    if argv[1].lower() == 'prd':
        from config import ProductionConfig
        cfg = ProductionConfig()
    elif argv[1].lower() == 'dev':
        from config import DevelopmentConfig
        cfg = DevelopmentConfig()
    else:
        from config import TestingConfig
        cfg = TestingConfig()

    zachbucket = minioOps(cfg)
    # metadata = {'x-amz-meta-testing': 'value'}
    # zachbucket.upload('aaa/shadw.png','D:\moban5001\img\image\shadow.png',metadata=metadata,content_type='application/x-png')
    zachbucket.getAllMetadataFromCurrentPath('')
    # file_path = "/mnt/d/video_test/egg_tart.mp4"
    # v = videoHandler(file_path)
    # metadata = v.get_mp4_info
    # project_name = 'CCTV'
    # minioPath = project_name + '/' + timeResolver.get_current_date() + '/'
    # zachbucket.upload(minioPath+basename(file_path), file_path, metadata=metadata,
    #                   content_type='application/video')
    # print(v.get_mp4_info)

    # print(zachbucket.getObjectFile('aaa/shadw.png',".\\shadw.png").getDownloadObjectInfo)

    # zachbucket.getObjectInfo('ds6')
    # zachbucket.statObjectInfo('server2.py')