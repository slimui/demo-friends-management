import json
from random import randint
from os import path
from ..models import db, User
from ..logging import logger
from sqlalchemy import func


def load_samples(checkfirst=True):
    if checkfirst and has_users():
        return
    load_sample_users()
    create_connections()


def load_sample_users():
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


def create_connections():
    users = dict([(u.user_id, u) for u in db.session.query(User).all()])
    n = db.session.query(func.count(User.user_id)).scalar()
    connectspecs = {
        'befriend': 12,
        'follow': 12,
        'block': 5
    }
    j = 0
    for x in range(1, n):
        user = users[x]
        for method, limit in connectspecs.items():
            for y in range(1, limit):
                other = users[randint(1, n)]
                if other == user:
                    continue
                try:
                    getattr(user, method)(other)
                    j += 1
                except:
                    pass
            db.session.flush()
    logger.info('Created {} user connections'.format(j))


def has_users():
    return db.session.query(func.count(User.user_id)).scalar()


def _load_json_file(*filepaths):
    with open(_relative_path(*filepaths), 'r') as fp:
        return json.load(fp)


def _relative_path(*filepaths):
    return path.join(path.dirname(path.realpath(__file__)), *filepaths)
