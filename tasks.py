from __future__ import absolute_import
from celery.task import task, Task
from celery.utils.log import get_task_logger
import os
import subprocess
from celery import Celery
import time
logger = get_task_logger(__name__)



class DebugTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        print('Task returned: {0!r}'.format(self.request))


@task( bind=True)
def error_handler(self, uuid):
    result = self.app.AsyncResult(uuid)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
        uuid, result.result, result.traceback))

@task(base=DebugTask, name="Sleep")
def sleep_task(sleep):
    #task will run sleep sec and return
    for t in xrange (sleep):
        #change task status (set name with percentage)
        sleep_task.update_state(state="PROCESSING %s%%" % (t*100/sleep))
        time.sleep(1)
    return 'OK'

