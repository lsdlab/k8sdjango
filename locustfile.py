import time
from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    @task(1)
    def ping_index(self):
        self.client.get("/ping/")

    @task(1)
    def cretate_user(self):
        self.client.post('/api/v1/users/email_password_signup/', {
            "email": str(time.time()) + "@gmail.com",
            "password": str(time.time()) + "@gmail.com"
            })

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://192.168.124.62:8080"
