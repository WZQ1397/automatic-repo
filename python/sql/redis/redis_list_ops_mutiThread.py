# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '..')
import pickle
import threading
import time
import os
import random
import shutil
import redis

origin_path = '/data/code/defect-tag-api/data/defect/static/test'
all_figure = os.listdir(origin_path)
a = random.sample(all_figure, 1)
exitFlag = 0
r = redis.StrictRedis(host='192.168.1.1', port=6379, db=10)


class myThread(threading.Thread):
    def __init__(self, camera_id, origin_path, counter=99999, batch_index=1):
        threading.Thread.__init__(self)
        self.camera_id = camera_id
        self.origin_path = origin_path
        self.dest_path = '/storage-data/origin'
        self.counter = counter
        self.batch_index = batch_index

    def run(self):
        batch_index = 2
        try:
            for i in range(100):
            # while 1:
                nn = self.camera_id
                for camera_id in range(1+(nn-1)*3, nn*3+1):
                    if camera_id in [1,4,7]:
                        is_normal = 0
                    else:
                        is_normal = random.randint(0, 1)
                    a = time.time()
                    file = random.sample(all_figure, 1)[0]
                    camera_id = camera_id
                    origin_path = self.origin_path + '/' + file
                    now_timestamp = int(time.time() * 1000)  # 毫秒时间戳
                    real_dest_origin_path = self.dest_path + '/' + str(camera_id) + '/' + str(
                        now_timestamp) + '.' + str(batch_index) + '.jpg'

                    shutil.copy(origin_path, real_dest_origin_path)
                    if is_normal == 1:
                        aaa = {'camera_id': camera_id, 'origin_path': real_dest_origin_path,
                               'is_normal': is_normal, 'result_info': '[]',
                               'heatmap_path': '',
                               'check_timestamp': int(time.time() * 1000) + random.randint(-200, 200),
                               'pic_save_time': int(time.time() * 1000) + random.randint(-200, 200),
                               'batch_index': batch_index,
                               'camera_status': 1}
                    else:
                        heatmap_path = '/storage-data/heatmap/{}.{}.jpg'.format(
                            int(time.time() * 1000),
                            batch_index)
                        shutil.copy('/data/code/defect-tag-api/data/defect/static/test_1/00022.png',
                                    heatmap_path)
                        aaa = {'camera_id': camera_id,
                               'origin_path': real_dest_origin_path,
                               'is_normal': is_normal, 'result_info': '[{"score": %s, "cls": 0}]' % random.random(),
                               'heatmap_path': heatmap_path,
                               'check_timestamp': int(time.time() * 1000) + random.randint(-200, 200),
                               'pic_save_time': int(time.time() * 1000) + random.randint(-200, 200),
                               'batch_index': batch_index,
                               'camera_status': 1}
                    r.lpush('detect_result_queue', pickle.dumps(aaa))
                batch_index += 1
                time.sleep(max((1 - float(time.time()) + float(a)),0))
                print(batch_index)
        except Exception as e:
            print(e)


# 创建新线程
# thread1 = myThread(camera_id, origin_path, dest_path)
thread1 = myThread(1, origin_path)
thread2 = myThread(2, origin_path)
thread3 = myThread(3, origin_path)
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print("out main ")
