from .utils import DBTest
from app.models import db, User
from app.errors import UserBlockedException


class UserModelTest(DBTest):

    def test_users(self):
        u = User(email='user@test,com', first_name="Test", last_name="User")
        db.session.add(u)
        db.session.commit()

        self.assertTrue(u in db.session)
        self.assertTrue(u.user_id)

        db.session.delete(u)
        db.session.commit()

        self.assertFalse(u in db.session)

    def test_befriending(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        u1.befriend(u2)
        db.session.commit()

        self.assertTrue(u1.is_friend_of(u2))
        self.assertFalse(u1.is_friend_of(u3))

        u1.unfriend(u2)
        db.session.commit()

        self.assertFalse(u1.is_friend_of(u2))

    def test_following(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u1.is_following(u3))

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))

    def test_mention(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        u1.mention(u2)
        db.session.commit()

        self.assertTrue(u1.has_mentioned(u2))
        self.assertFalse(u1.has_mentioned(u3))

        u1.unmention(u2)
        db.session.commit()

        self.assertFalse(u1.has_mentioned(u2))

    def test_blocking(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        u1.block(u2)
        db.session.commit()

        self.assertTrue(u1.is_blocking(u2))
        self.assertFalse(u1.is_blocking(u3))

        # Test befriending/following in context of blocking
        self.assertTrue(u3.befriend(u1))
        self.assertTrue(u3.follow(u1))
        with self.assertRaises(UserBlockedException):
            u2.befriend(u1)
        with self.assertRaises(UserBlockedException):
            u2.follow(u1)

        u1.unblock(u2)
        db.session.commit()

        self.assertTrue(u2.befriend(u1))
        self.assertTrue(u2.follow(u1))
