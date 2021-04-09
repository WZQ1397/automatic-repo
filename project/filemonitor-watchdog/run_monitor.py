import os
import time
import traceback
from threading import Thread
import MySQLdb
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import config


def mysql_initial():
    conn = MySQLdb.connect(host=config.MYSQL_HOST, user=config.MYSQL_USER, password=config.MYSQL_PASS,
                           db=config.MYSQL_DB, port=config.MYSQL_PORT, autocommit=True, charset="utf8")
    return conn


def insert_sql(conn, sql, values):
    try:
        cur = conn.cursor()
        cur.executemany(sql, values)
        conn.commit()
        return "insert mysql: OK"
    except:
        conn.rollback()
        traceback.print_exc()
    finally:
        cur = conn.cursor()
        cur.close()


values = list()


class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, **kwargs):
        super(FileMonitorHandler, self).__init__(**kwargs)
        self._watch_path = config.WATCH_PATH

    def on_created(self, event):
        print('monitor new file:', event.src_path)
        file = event.src_path
        # print(event.src_path)
        # print(file.split("/")[-5:])
        file_time = int(os.path.getctime(file))
        project, shop, _, camera, file_name = file.split("/")[-5:]
        try:
            data = [int(project), int(shop), int(camera), file_name, file, file_time]
        except Exception as e:
            data = []
            print(e)
        values.append(data)
        print(values)


def insert(values):
    conn = mysql_initial()
    sql = """
        INSERT INTO img_info (project, shop, camera, image_name, image_path, timestamp) VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE image_path=VALUES(image_path),timestamp=VALUES(timestamp)
    """
    insert_sql(conn, sql, values)
    print("insert done, values: ", values)


def main(path):
    t = path.split("/")[-1]
    timeArray = time.strptime(t, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    stop_time = timeStamp + 60*60*24 + 60*30
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print("Monitoring path: {} ...".format(path))
    try:
        while True:
            tp = int(time.time())
            time.sleep(1)
            global values
            if tp % 15 == 0 and len(values) > 0:  # Insert MySQL every 15 seconds if value has something
                insert(values)
                values = list()
            if tp > stop_time:  # 监控持续到第二天的0:30
                observer.stop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def get_monitored_list():
    t = time.time()
    timeArray = time.localtime(t)
    f_date = time.strftime("%Y-%m-%d", timeArray)
    monitor_path = list()
    file_path_list = os.listdir(config.WATCH_PATH)
    for x in file_path_list:
        path_proj = '/'.join([config.WATCH_PATH, x])
        file_path_list_proj = os.listdir(path_proj)
        for x in file_path_list_proj:
            path_shop = '/'.join([path_proj, x])
            path_date = os.listdir(path_shop)
            if f_date in path_date:
                monitor_path.append("/".join([path_shop, f_date]))
    return set(monitor_path)


def create_task(file_path):
    for path in file_path:
        thread = Thread(target=main, name="monitor_{}".format(path), args=(path,))
        thread.start()


if __name__ == "__main__":
    file_path = get_monitored_list()
    print(file_path)
    create_task(file_path)
    while True:
        t = int(time.time())
        time.sleep(1)
        if t % 5 == 0:
            file_path_2 = get_monitored_list()
            new_file_path = file_path_2 - file_path
            create_task(new_file_path)
            file_path = file_path_2


# [1, 14, 3, '1560747502_imi_3_001.jpg', '/DATA5_DB8/data/check_image/1/14/2019-06-17/3/1560747502_imi_3_001.jpg', 1560753944]]
