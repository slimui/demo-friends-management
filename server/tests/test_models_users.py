from .utils import DBTest
from app.models import db, User, common_friends_between
from app.errors import UserBlockedException
from app.logging import logger  # noqa


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
        db.session.flush()
        u1.befriend(u2)
        db.session.commit()

        self.assertTrue(u1.is_friend_of(u2))
        self.assertTrue(u2 in u1.friends.all())
        self.assertFalse(u1.is_friend_of(u3))

        u1.unfriend(u2)
        db.session.commit()

        self.assertFalse(u1.is_friend_of(u2))
        self.assertFalse(u2 in u1.friends.all())

    def test_following(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.flush()
        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2 in u1.following.all())
        self.assertTrue(u1 in u2.followers.all())
        self.assertFalse(u1.is_following(u3))

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2 in u1.following.all())
        self.assertFalse(u1 in u2.followers.all())

    def test_blocking(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.flush()
        u1.block(u2)
        db.session.commit()

        self.assertTrue(u1.is_blocking(u2))
        self.assertTrue(u2 in u1.blocked.all())
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

    def test_subscribing(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()

        self.assertFalse(u2 in u1.subscribing.all())
        self.assertFalse(u1.is_subscribing(u2))
        self.assertFalse(u3 in u1.subscribing.all())
        self.assertFalse(u1.is_subscribing(u3))
        self.assertFalse(u1 in u2.subscribers.all())
        self.assertFalse(u1 in u3.subscribers.all())

        u1.befriend(u2)
        u1.follow(u3)
        db.session.flush()
        self.assertTrue(u2 in u1.subscribing.all())
        self.assertTrue(u1.is_subscribing(u2))
        self.assertTrue(u3 in u1.subscribing.all())
        self.assertTrue(u1.is_subscribing(u3))
        self.assertTrue(u1 in u2.subscribers.all())
        self.assertTrue(u1 in u3.subscribers.all())

        u1.block(u2)
        db.session.flush()
        self.assertFalse(u2 in u1.subscribing.all())
        self.assertFalse(u1.is_subscribing(u2))
        self.assertFalse(u1 in u2.subscribers.all())
        self.assertTrue(u3 in u1.subscribing.all())
        self.assertTrue(u1.is_subscribing(u3))
        self.assertTrue(u1 in u3.subscribers.all())

        u1.unblock(u2)
        db.session.flush()
        self.assertTrue(u2 in u1.subscribing.all())
        self.assertTrue(u1 in u2.subscribers.all())

    def test_common_friends(self):
        u1 = User(email='user1@test.com')
        u2 = User(email='user2@test.com')
        u3 = User(email='user3@test.com')
        u4 = User(email='user4@test.com')
        u5 = User(email='user5@test.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.add(u5)
        db.session.flush()
        u1.befriend(u2)  # u1 friends
        u1.befriend(u3)
        u1.befriend(u4)
        u2.befriend(u1)  # u2 friends
        u2.befriend(u3)
        u3.befriend(u2)  # u3 friends
        u3.befriend(u5)
        u4.befriend(u1)  # u4 friends
        u5.befriend(u1)  # u5 friends
        u5.befriend(u2)
        u5.befriend(u3)
        u5.befriend(u4)
        db.session.commit()

        friends = common_friends_between(1, [2, 3, 4, 5])
        # u2 common friends
        self.assertEqual(friends[0][0], 2)
        self.assertEqual(friends[0][1], [3])
        # u3 common friends
        self.assertEqual(friends[1][0], 3)
        self.assertEqual(friends[1][1], [2])
        # u4 common friends
        self.assertEqual(friends[2][0], 4)
        self.assertEqual(friends[2][1], [])
        # u5 common friends
        self.assertEqual(friends[3][0], 5)
        self.assertEqual(friends[3][1], [2, 3, 4])
