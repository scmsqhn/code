#!

# celery config
#BROKER_URL = 'amqp://'
#CELERY_RESULT_BACKEND = 'amqp://'
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
#CELERY_IMPORTS = ("tasks",)


## Broker settings.
#broker_url = 'amqp://guest:guest@localhost:5672//'
broker_url = 'redis://:localhost:6379/0'

# List of modules to import when the Celery worker starts.
#imports = ('myapp.tasks',)

## Using the database to store task state and results.
result_backend = 'redis://:localhost:6379/0'
#result_backend = 'db+sqlite:///results.db'

#task_annotations = {'tasks.add': {'rate_limit': '10/s'}}
