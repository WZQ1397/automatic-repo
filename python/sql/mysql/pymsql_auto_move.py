import random
import os, re
import shutil
import time
import traceback

import pymysql
pymysql.install_as_MySQLdb()
import datetime
connt= pymysql.connect(host='192.168.1.1',port=3306,user='haor',password='123456',database='zach_tag')
cursor=connt.cursor()



def auto_camera():
    try:
        for i in range(1, 10):
            origin_path = '/data/code/zach-tag-api/data/zach/static/test'
            origin_heatmap_path = '/data/code/zach-tag-api/data/zach/static/test_1'

            dest_path = '/storage-data/camera'
            heatmap_path = '/storage-data/heatmap' # 热力图静态资源地址
            all_figure = os.listdir(origin_path)
            all_heatmap_path = os.listdir(origin_heatmap_path)
            random_file = random.sample(all_figure, 2)
            random_heat_file = random.sample(all_heatmap_path, 2)

            exitFlag = 0
            now_timestamp = int(time.time() * 1000)  # 毫秒时间戳
            file = random_file[0]
            heatmap = random_heat_file[1]
            origin_path = origin_path + '/' + file
            heatmap_path_1 = origin_heatmap_path+ '/' + heatmap

            dest_path = dest_path + '/{}'.format(i) + '/' + str(now_timestamp) + '.jpg'
            heatmap_path = heatmap_path + '/' + str(now_timestamp) + '.jpg'

            shutil.copy(origin_path, dest_path)
            shutil.copy(heatmap_path_1, heatmap_path)
            is_normal = 1 if i != 8 else 0
            score = random.random()
            if is_normal == 1:
                print(dest_path)
                print(heatmap_path)
                sql = "select * from camera_current_result where camera_id = {}".format(i)
                cursor.execute(sql)
                res = cursor.fetchone()
                if res:
                    sql = """update  camera_current_result set camera_id='{}' , origin_path = '{}',heatmap_path='{}',is_normal='1',result_info='{}',update_timestamp='{}' where camera_id='{}'""".format(i,dest_path,heatmap_path,str([]),time.time(),i)
                    cursor.execute(sql)
                else: #新增一个
                    sql = """insert into camera_current_result(camera_id,origin_path,heatmap_path,is_normal,result_info,update_timestamp) values('{}','{}','{}',1,'{}','{}')""".format(i,dest_path,heatmap_path,str([]),time.time())
                    cursor.execute(sql)
            else:
                sql = "select * from camera_current_result where camera_id = {}".format(i)
                cursor.execute(sql)
                res = cursor.fetchone()
                print(dest_path)
                print(heatmap_path)
                if res:
                    sql = """update  camera_current_result set camera_id='{}' , origin_path ='{}',heatmap_path='{}',is_normal='0',result_info="{}",update_timestamp={} where camera_id='{}'""".format(i,dest_path,heatmap_path,str([{ 'cls': 0, 'score': score, 'heatmap_src': heatmap_path}]),time.time(),i)
                    cursor.execute(sql)
                else: #新增一个
                    sql = 'insert into camera_current_result(camera_id,origin_path,heatmap_path,is_normal,result_info,update_timestamp) values("{}","{}","{}",0,"{}","{}")'.format(i,dest_path,heatmap_path,str([{ 'cls': 0, 'score': score, 'heatmap_src': heatmap_path}]),time.time())
                    cursor.execute(sql)
            connt.commit()

        print('shoot______________________')
    except Exception as e:
        traceback.print_exc()
        print(e)
while 1:
    auto_camera()
    time.sleep(1)
