import json
from os import path
from ..models import db, User
from ..logging import logger
from sqlalchemy import func


def load_sample_users(checkfirst=True):
    if checkfirst:
        n = db.session.query(func.count(User.user_id)).scalar()
        if n:
            logger.info('Skipping load sample users')
            return
    db.session.query(User).delete()
    n = 0
    for data in _load_json_file('users.json'):
        user = User(**data)
        db.session.add(user)
        n += 1
        if n % 20:
            db.session.flush()
    if n % 20:
        db.session.flush()
    logger.info('Loaded {} sample users'.format(n))


def _load_json_file(*filepaths):
    with open(_relative_path(*filepaths), 'r') as fp:
        return json.load(fp)


def _relative_path(*filepaths):
    return path.join(path.dirname(path.realpath(__file__)), *filepaths)
