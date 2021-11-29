# -*- coding=utf-8 -*-
import threading
import time
import os
import random
import shutil
import traceback

origin_path = '/data/code/defect-tag-api/data/defect/static/test'
all_figure = os.listdir(origin_path)
a = random.sample(all_figure,1)
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, camera_id, origin_path, dest_path,counter=99999):
        threading.Thread.__init__(self)
        self.camera_id = camera_id
        self.origin_path = origin_path
        self.dest_path = dest_path
        self.counter = counter
    def run(self):
        try:
            print ("begin:" + str(self.camera_id))
            move_file(self.origin_path, self.dest_path,self.counter)
            print ("over:" + str(self.camera_id))
        except Exception as e:
            traceback.print_exc()
            print(e)
def move_file(origin_path, dest_path, counter):
    while counter:
        try:
            now_timestamp = int(time.time() * 1000)  # 毫秒时间戳
            file = random.sample(all_figure, 1)[0]
            shutil.copy(origin_path+'/'+file, dest_path+'/'+str(now_timestamp)+'.jpg')
            time.sleep(0.2)
            print('---------')
        except Exception as e:
            traceback.print_exc()
            print(e)

# 创建新线程
# thread1 = myThread(camera_id, origin_path, dest_path)
thread1 = myThread(1, origin_path, "/zach-ramdisk/dev/camera/1")
thread2 = myThread(2, origin_path, "/zach-ramdisk/dev/camera/2")
thread3 = myThread(3, origin_path, "/zach-ramdisk/dev/camera/3")
thread4 = myThread(4, origin_path, "/zach-ramdisk/dev/camera/4")
thread5 = myThread(5, origin_path, "/zach-ramdisk/dev/camera/5")
thread6 = myThread(6, origin_path, "/zach-ramdisk/dev/camera/6")
thread7 = myThread(7, origin_path, "/zach-ramdisk/dev/camera/7")
thread8 = myThread(8, origin_path, "/zach-ramdisk/dev/camera/8")
thread9 = myThread(9, origin_path, "/zach-ramdisk/dev/camera/9")
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
print ("out main ")
