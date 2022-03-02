
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from general import model

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(100))
    password = sa.Column(sa.String(400))

    def to_model(self, with_password: bool = False) -> model.User:
        result = model.User(
            id=self.id,
            username=self.username
        )
        if with_password:
            result.password = self.password

        return result
