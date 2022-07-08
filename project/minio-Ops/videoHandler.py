import cv2

class videoHandler:
    def __init__(self, file_path, video_info={}):
        self.file_path = file_path
        self.video_info = video_info

    @property
    def get_mp4_info(self) -> dict:
        cap = cv2.VideoCapture(self.file_path)
        if cap.isOpened():
            self.video_info['weight'] = cap.get(3)
            self.video_info['height'] = cap.get(4)
            rate = cap.get(5)
            frame_number = cap.get(7)
            seconds = frame_number / rate
            self.video_info['length'] = seconds
            return self.video_info
        else:
            return None

    @staticmethod
    def translate_seconds_to_hms(seconds, str=True):
        h = seconds // 3600
        m = seconds % 3600 // 60
        s = seconds % 60
        if str:
            return '{:.0f}时{:.0f}分{:.2f}秒'.format(h, m, s)
        else:
            return h, m, s

    def __str__(self):
        content = ''
        for k, v in self.get_mp4_info().items():
            content += f'{k} => {v}\n'
        return content


if __name__ == '__main__':
    file_path = "/mnt/d/video_test/egg_tart.mp4"
    v = videoHandler(file_path)
    print(v.get_mp4_info)