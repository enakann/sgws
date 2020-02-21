#locust -f loadtest.py --slave
#locust - f loadtest.py - -master

from locust import HttpLocust, TaskSet, task, between


def index(l):
    l.client.get("/")

def stats(l):
    l.client.get("/echo_request")

class UserTasks(TaskSet):
    # one can specify tasks like this
    #itasks = [index, stats]

    # but it might be convenient to use the @task decorator
    @task
    def index(self):
        self.client.get("/sgws/sg/forward")

class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    host = "http://127.0.0.1:8082"
    wait_time = between(2, 5)
    task_set = UserTasks
