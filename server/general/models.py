
import sqlalchemy as sa

from curriculum.models import BaseModel  # TODO: there's gotta be a better way


class User(BaseModel):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
