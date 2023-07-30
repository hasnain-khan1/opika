## Flask app with rabbiqMQ and Celery

This app is created using Flask and Celery for the queueing system. RabbitMQ is used as a broker. This app will scrap the data from hacker news API which is a free API and will store the top news data in a local `.db` file.

## Installation

Install the  [Docker](https://docs.docker.com/engine/install/) according to your OS.

## Usage
Set the up the Celery app configurations
```python
celery_app = Celery('simple_worker',
                    broker=f'amqp://{user}:{password}@{ip}:5672',
                    backend='rpc://')

```
Go to the main directory of the project and run the command
```bash
docker-compose up
```
This set up the docker container and You can access the app on Following URL:
```
htpp://localhost:5000
```

## Run the Tests

To run the pytests go to the main project directory and run the following command.
```bash
pytest tests/
```

It will start all the tests inside the tests directory.