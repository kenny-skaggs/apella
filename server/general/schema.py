
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from general import model

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(100))
    email = sa.Column(sa.String(200))
    password = sa.Column(sa.String(400))

    first_name = sa.Column(sa.String(200))
    last_name = sa.Column(sa.String(200))

    def to_model(self, with_password: bool = False, with_roles=False) -> model.User:
        result = model.User(
            id=self.id,
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name
        )
        if with_password:
            result.password = self.password
        if with_roles:
            result.roles = [ref.role.name for ref in self.role_refs]

        return result


class Role(BaseModel):
    __tablename__ = 'role'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80))


class UserRole(BaseModel):
    __tablename__ = 'user_role'
    id = sa.Column(sa.Integer, primary_key=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    user = relationship(User, backref='role_refs')

    role_id = sa.Column(sa.Integer, sa.ForeignKey(Role.id))
    role = relationship(Role, backref='user_refs')
