from .utils import DBTest
from app.models import db, User
import json
import os

class TestSampleTest(DBTest):

    def test_samples(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        f = os.path.join(cwd, 'MOCK_DATA.json')
        with open(f, 'r') as fp:
            data = json.load(fp)
        users = []
        i = 0
        for item in data:
            item['user_id'] = item['id']
            del item['id']
            sex = item['gender'] == 'Male' and 'men' or 'women'
            item['avatar_url'] = 'https://randomuser.me/api/portraits/{}/{}.jpg'.format(sex, item['user_id'] - 1)
            i += 1
            users.append(item)
            if i == 100:
                break
        f = os.path.join(cwd, 'data.json')
        with open(f, 'w') as fp:
            json.dump(users, fp, indent=2)
