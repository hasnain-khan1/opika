from flask import Flask
from celery import Celery

flask_obj = Flask(__name__)
"""
Celery setting for rabbitMQ.it requires user:password@ip to connect to its server.
For backend I am using celery default rpc,
"""
celery_app = Celery('simple_worker',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='rpc://')


@flask_obj.route('/task_result/<task_id>')
def task_result(task_id):
    """ Function to check the result against the task id """
    result = celery_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)


@flask_obj.route('/task_status/<task_id>')
def get_status(task_id):
    """
    Function to check the task status.
    status are pending, running and complete
    """
    status = celery_app.AsyncResult(task_id, app=celery_app)
    return "Status of the Task " + str(status.state)


@flask_obj.route('/start_task')
def call_method():
    """
    This will add the tasks to celery queue and return the task id.
    :return:
    """
    flask_obj.logger.info("Sending tasks to Celery Worker")
    r = celery_app.send_task('tasks.longtime_add')
    flask_obj.logger.info(r.backend)
    return r.id

