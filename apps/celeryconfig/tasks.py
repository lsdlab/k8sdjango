from celery.decorators import task, periodic_task
from celery.task.schedules import crontab


@task(name="hello")
def hello():
    return 'hello world'


@task(name="sum_two_numbers")
def add(x, y):
    return x + y


@task(name="mul_two_numbers")
def mul(x, y):
    return x * y


# crontab() means run every 10 seconds
@periodic_task(name="periodic_task", run_every=crontab())
def periodic_task():
    print('periodic task test!!!!!')
    print('success')
    return True
