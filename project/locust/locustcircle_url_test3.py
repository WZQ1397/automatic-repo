from locust import TaskSet, task, HttpLocust
import queue
class UserBehavior(TaskSet):
    @task
    def test_register(self):
        try:
            data = self.locust.user_data_queue.get()
        except queue.Empty:
            print('account data run out, test ended.')
            exit(0)
        print('register with user: {}, pwd: {}'\
            .format(data['username'], data['password']))
        payload = {
            'username': data['username'],
            'password': data['password']
        }
        self.client.post('/register', data=payload)
        self.locust.user_data_queue.put_nowait(data)
        
#TODO 保证并发测试数据唯一性，循环取数据
class WebsiteUser(HttpLocust):
    host = 'http://debugtalk.com'
    task_set = UserBehavior
    user_data_queue = queue.Queue()
    for index in range(100):
        data = {
            "username": "test%04d" % index,
            "password": "pwd%04d" % index,
            "email": "test%04d@debugtalk.test" % index,
            "phone": "186%08d" % index,
        }
        user_data_queue.put_nowait(data)
    min_wait = 1000
    max_wait = 3000