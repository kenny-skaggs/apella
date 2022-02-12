
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(100))
    password = sa.Column(sa.String(400))
