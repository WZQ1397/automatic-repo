# 166
# Author: Zach.Wang
import os
import time

START_CAM=1
END_CAM=9

RAMDISK_BASE_PATH="/zach-ramdisk/"
RAMDISK_STATIC_DATA_BASE_PATH="data/static/"
RAMDISK_TTAS_DATA_PATH=f"{RAMDISK_BASE_PATH}{RAMDISK_STATIC_DATA_BASE_PATH}"
INPUT_CAMERA_PATH = f'{RAMDISK_TTAS_DATA_PATH}/camera'  # 输入相机目录
INPUT_HEATMAP_PATH = f'{RAMDISK_TTAS_DATA_PATH}/heatmap' # 输入热力图路径

DATA_STORAGE_BASE_PATH='/storage-data/'
DATA_STORAGE_TTAS_DATA_PATH=DATA_STORAGE_BASE_PATH
DATA_STORAGE_HEATMAP_PATH = f'{DATA_STORAGE_TTAS_DATA_PATH}/heatmap'
DATA_STORAGE_ORI_PATH = f'{DATA_STORAGE_TTAS_DATA_PATH}/origin'
DATA_STORAGE_SHOOT_PATH = f'{DATA_STORAGE_TTAS_DATA_PATH}/shoot'

NEED_CLEAN_CONFIG_MAP = {
    "BASE":50,
    "RAMDISK":{
        INPUT_CAMERA_PATH:15,
        INPUT_HEATMAP_PATH:100
    },
    "STORAGE_DISK": {
        DATA_STORAGE_HEATMAP_PATH: 1000,
        DATA_STORAGE_ORI_PATH: 1000,
        DATA_STORAGE_SHOOT_PATH: 1000
    }
}

def clean(START_CAM=1,END_CAM=9,TYPE="STORAGE_DISK", FILE_NAME_RANGE=13):
    '''
    :param START_CAM: default 1
    :param END_CAM: default 9
    :param TYPE: "STORAGE_DISK"
    :param FILE_NAME_RANGE: 13
    :return: None
    '''
    END_CAM+=1
    for i in range(START_CAM,END_CAM):
        try:
            for PATH,SAVE_NUMS in NEED_CLEAN_CONFIG_MAP[TYPE].items():
                PATH=f'{PATH}/{i}'
                count=0
                try:
                    file_list = os.listdir(f'{PATH}/')
                    file_list.sort(key=lambda x: int(x[:FILE_NAME_RANGE]))
                    if len(file_list) > NEED_CLEAN_CONFIG_MAP["BASE"]+SAVE_NUMS:
                        for file in file_list[:-NEED_CLEAN_CONFIG_MAP["BASE"]]:
                            os.remove(f'{PATH}/{str(file)}')
                            count+=1
                except Exception as e:
                    print(e)
                finally:
                    print(f'Has cleaned {TYPE} => {PATH} | CAMERA-{i}: {count} deleted!')
        except IndexError as e:
            print(e)

try:
    while True :
        clean(TYPE="RAMDISK")
        clean(TYPE="STORAGE_DISK")
        time.sleep(10)
except Exception as e:
    print(e)