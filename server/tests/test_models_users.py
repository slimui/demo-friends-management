import os
from .utils import DBTest
from app.models import (db, User)
from sqlalchemy import func


class UserModelTest(DBTest):

    def test_changelogs(self):
        u = User(email='user@test,com', first_name="Test", last_name="User")
        db.session.add(u)
        db.session.commit()

        assert u in db.session
        assert u.user_id

        db.session.delete(u)
        db.session.commit()

        assert u not in db.session
