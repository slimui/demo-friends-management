import logging
# from flask import current_app
# from werkzeug.local import LocalProxy
# logger = LocalProxy(lambda: current_app.logger)

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
