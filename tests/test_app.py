# test_app.py


import pytest
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask_app.app import app, simple_app


@pytest.fixture
def celery_worker():
    return simple_app.Worker()


@pytest.fixture(autouse=True)
def setup_and_teardown_tasks(celery_worker):
    celery_worker.start()
    yield
    celery_worker.stop()


@pytest.fixture
def test_client():
    with app.test_client() as client:
        yield client


def test_call_method(test_client):
    response = test_client.get('/start_task')
    assert response.status_code == 200


def test_get_status(test_client):
    # Perform the necessary steps to create a task and obtain its ID
    # Then, use the obtained task_id to test the '/task_status/<task_id>' endpoint
    task_id = 'task_id_here'  # Replace this with the actual task ID
    response = test_client.get(f'/task_status/{task_id}')
    assert response.status_code == 200
    # Add more assertions as needed based on your specific use case


def test_task_result(test_client):
    # Perform the necessary steps to create a task and obtain its ID
    # Then, use the obtained task_id to test the '/task_result/<task_id>' endpoint
    task_id = 'task_id_here'
    response = test_client.get(f'/task_result/{task_id}')
    assert response.status_code == 200
    # Add more assertions as needed based on your specific use case
