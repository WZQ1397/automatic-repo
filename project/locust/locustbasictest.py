from locust import HttpLocust, TaskSet, task

def index(l):
    l.client.get("/")
    #self.client.post("/login", {"username":"ellen_key", "password":"education"})

def stats(l):
    l.client.get("/admin.php")

class UserTasks(TaskSet):
    #weight = 1
    # one can specify tasks like this
    tasks = [index, stats]
    
    # for weight
    #tasks = {index:3, stats:1}
    
    # but it might be convenient to use the @task decorator
    @task
    def page404(self):
        self.client.get("/error")
'''
class UserTasks2(TaskSet):
    weight = 3
    # one can specify tasks like this
    tasks = [index, stats]

    # but it might be convenient to use the @task decorator
    @task
    def page404(self):
        self.client.get("/error")
'''  
class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    host = "http://172.16.10.120:8089"
    min_wait = 2000
    max_wait = 5000
    task_set = UserTasks