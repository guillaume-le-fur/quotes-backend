import datetime

from werkzeug.security import generate_password_hash

from models.tag import TagModel
from models.user import UserModel
from models.quote import QuoteModel
import uuid


def populate():
    if UserModel.query.count() == 0:
        user1 = UserModel(
            public_id=str(uuid.uuid4()),
            username="User 1",
            email="a@a.a",
            password=generate_password_hash("aaaaaa", method='sha256'),
            is_admin=False
        )
        user2 = UserModel(
            public_id=str(uuid.uuid4()),
            username="User 2",
            email="b@b.b",
            password=generate_password_hash("bbbbbb", method='sha256'),
            is_admin=True
        )
        [user.save_to_db() for user in [user1, user2]]

        tag1 = TagModel(name="war")
        tag2 = TagModel(name="peace")
        tag3 = TagModel(name="fantasy")
        tag4 = TagModel(name="dummyTag")

        [tag.save_to_db() for tag in [tag1, tag2, tag3, tag4]]

        quote1 = QuoteModel(
            creator_id=1,
            text="Alea iacta est",
            author="Julius Caesar",
            book="Da vita Caesarum",
            creation_date=datetime.datetime.now()
        )

        quote1.tags = [tag1, tag2]

        quote2 = QuoteModel(
            creator_id=1,
            text="Dummy 1",
            author="User 1",
            book="Quotes, vol 1",
            creation_date=datetime.datetime.now()
        )

        quote2.tags = [tag3]

        quote3 = QuoteModel(
            creator_id=2,
            text="Dummy 2",
            author="User 2",
            book="Quotes, vol 2",
            creation_date=datetime.datetime.now()
        )

        quote3.tags = [tag4]

        [quote.save_to_db() for quote in [quote1, quote2, quote3]]
