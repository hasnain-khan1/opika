import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask_app.app import flask_obj, celery_app
from unittest.mock import Mock


@pytest.fixture
def client():
    flask_obj.config['TESTING'] = True
    with flask_obj.test_client() as client:
        yield client


def test_call_method(client, mocker):
    # Mock the Celery task
    task_mock = Mock()
    task_mock.id = 'awe5t-5mslflk-34rln64tyr'

    mocker.patch('flask_app.app.celery_app.send_task', return_value=task_mock)

    # Make a request to the Flask route
    response = client.get('/start_task')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the content of the response is the task ID
    assert response.get_data(as_text=True) == task_mock.id

    # Assert that the send_task method was called with the correct task name
    celery_app.send_task.assert_called_once_with('tasks.longtime_add')


def test_get_status(client, mocker):
    # Mock the AsyncResult object returned by Celery
    async_result_mock = Mock()
    async_result_mock.state = 'SUCCESS'  # Set the state to a sample value, you can change this as needed
    mocker.patch('flask_app.app.celery_app.AsyncResult', return_value=async_result_mock)

    # Make a request to the Flask route with a task ID
    task_id = 'awe5t-5mslflk-34rln64tyr'
    response = client.get(f'/task_status/{task_id}')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the content of the response
    expected_response = f"Status of the Task {async_result_mock.state}"
    assert response.get_data(as_text=True) == expected_response

    # Assert that the AsyncResult was called with the correct task ID and app
    celery_app.AsyncResult.assert_called_once_with(task_id, app=celery_app)


def test_task_result(client, mocker):
    # Mock the AsyncResult object returned by Celery
    async_result_mock = Mock()
    async_result_mock.result = 42  # Set the result to a sample value
    mocker.patch('flask_app.app.celery_app.AsyncResult', return_value=async_result_mock)

    # Make a request to the Flask route with a task ID
    task_id = 'awe5t-5mslflk-34rln64tyr'
    response = client.get(f'/task_result/{task_id}')

    # Assert the response status code
    assert response.status_code == 200

    # Assert that the AsyncResult was called with the task ID
    celery_app.AsyncResult.assert_called_once_with(task_id)
