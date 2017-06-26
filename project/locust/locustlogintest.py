from lxml import etree
from locust import TaskSet, task, HttpLocust

class UserBehavior(TaskSet):
    @staticmethod
    def get_session(html):
        tree = etree.HTML(html)
        return tree.xpath("//div[@class='XXXX']/input[@name='session']/@value")[0]
    @task(10)
    def test_login(self):
        html = self.client.get('/login').text
        #TODO login
        username = 'XXXXXX'
        password = '123456'
        session = self.get_session(html)
        payload = {
            'username': username,
            'password': password,
            'session': session
        }
        self.client.post('/login', data=payload)
        
class WebsiteUser(HttpLocust):
    host = 'http://debugtalk.com'
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
