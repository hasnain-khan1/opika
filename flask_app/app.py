from flask import Flask
from celery import Celery

flask_obj = Flask(__name__)
celery_app = Celery('simple_worker',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='rpc://')


@flask_obj.route('/task_result/<task_id>')
def task_result(task_id):
    result = celery_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)


@flask_obj.route('/task_status/<task_id>')
def get_status(task_id):
    status = celery_app.AsyncResult(task_id, app=celery_app)
    return "Status of the Task " + str(status.state)


@flask_obj.route('/start_task')
def call_method():
    flask_obj.logger.info("Sending tasks to Celery Worker")
    r = celery_app.send_task('tasks.longtime_add')
    flask_obj.logger.info(r.backend)
    return r.id

