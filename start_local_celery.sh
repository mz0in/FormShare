celery -A formshare.config.celery_app worker --loglevel=error --broker=amqp://formshare:formshare@localhost:5672/formshare --result-backend=rpc://formshare:formshare@localhost:5672/formshare
