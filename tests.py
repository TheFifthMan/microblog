import unittest
from datetime import datetime, timedelta
from app import db,app
from app.models import User,Post

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:qwe123@127.0.0.1/devmicroblog"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatars(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
                                         
    def test_follow(self):
        john = User(username='john',email='john@example.com')
        susan = User(username='susan',email='susan@example.com')
        mary = User(username='mary',email='mary@example.com')
        jack = User(username='jack',email='jack@example.com')

        db.session.add(john)
        db.session.add(susan)
        db.session.add(jack)
        db.session.add(mary)
        

        db.session.commit()


        john.follow(susan)
        john.follow(mary)
        john.follow(jack)

        susan.follow(mary)
        susan.follow(jack)

        mary.follow(jack)

        jack.follow(john)

        db.session.commit()

        self.assertTrue(john.is_following(susan))
        self.assertTrue(john.is_following(mary))
        self.assertTrue(john.is_following(jack))

        self.assertTrue(susan.is_following(mary))
        self.assertTrue(susan.is_following(jack))

        self.assertTrue(mary.is_following(jack))
        self.assertTrue(jack.is_following(john))

        self.assertEqual(jack.followed.first().username,'john')
        self.assertEqual(mary.followed.first().username,'jack')

    
    def test_unfollow(self):
        john = User(username='john',email='john@example.com')
        susan = User(username='susan',email='susan@example.com')
        mary = User(username='mary',email='mary@example.com')
        jack = User(username='jack',email='jack@example.com')

        db.session.add(john)
        db.session.add(susan)
        db.session.add(jack)
        db.session.add(mary)
        

        db.session.commit()


        john.follow(susan)
        john.follow(mary)
        john.follow(jack)
        john.unfollow(jack)

        susan.follow(mary)
        susan.unfollow(mary)

        susan.follow(jack)

        mary.follow(jack)

        jack.follow(john)

        db.session.commit()

        self.assertTrue(john.is_following(susan))
        self.assertTrue(john.is_following(mary))
        self.assertFalse(john.is_following(jack))

        self.assertFalse(susan.is_following(mary))
        self.assertTrue(susan.is_following(jack))

        self.assertTrue(mary.is_following(jack))
        self.assertTrue(jack.is_following(john))
    
    def test_followed_posts(self):
        john = User(username='john',email='john@example.com')
        susan = User(username='susan',email='susan@example.com')
        mary = User(username='mary',email='mary@example.com')
        jack = User(username='jack',email='jack@example.com')
        db.session.add_all([john,susan,mary,jack])

        now = datetime.now()
        p1 = Post(body='body from john',author=john,timestamp=now)
        p2 = Post(body='body from susan',author=susan,timestamp=now+timedelta(seconds=1))
        p3 = Post(body='body from mary',author=mary,timestamp=now+timedelta(seconds=2))
        p4 = Post(body='body from jack',author=jack,timestamp=now+timedelta(seconds=3))

        db.session.add_all([p1,p2,p3,p4])
        db.session.commit()
        john.follow(susan)
        john.follow(mary)
        john.follow(jack)

        mary.follow(jack)
        jack.follow(john)

        db.session.commit()

        followed_posts = john.followed_posts().all()
        self.assertIn(p1,followed_posts)
        self.assertIn(p2,followed_posts)
        self.assertIn(p3,followed_posts)
        self.assertIn(p4,followed_posts)

        followed_posts2 = mary.followed_posts().all()
        self.assertNotIn(p1,followed_posts2)
        self.assertIn(p3,followed_posts2)
        self.assertIn(p4,followed_posts2)




if __name__ == "__main__":
    unittest.main(verbosity=2)