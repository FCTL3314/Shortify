from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.extensions import db
from app.main.models import Url
from app.users.models import User


class TestObject(ABC):

    @abstractmethod
    def create(self, **kwargs):
        pass


@dataclass(frozen=True)
class TestUser(TestObject):
    username: str = 'TestUser'
    email: str = 'email@example.com'
    password: str = 'TestPassword'
    first_name: str = 'Test'
    last_name: str = 'User'
    slug: str = 'testuser'

    wrong_password: str = '123'

    def create(self, **kwargs):
        defaults = {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
        }
        defaults.update(kwargs)

        user = User(**defaults)
        db.session.add(user)
        db.session.commit()
        return user


@dataclass(frozen=True)
class TestUrl(TestObject):
    original_url: str = 'https://example.com'

    def create(self, **kwargs):
        defaults = {
            'original_url': self.original_url,
        }
        defaults.update(kwargs)

        url = Url(**defaults)
        db.session.add(url)
        db.session.commit()
        return url
