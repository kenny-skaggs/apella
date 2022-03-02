from typing import Sequence

from sqlalchemy.orm import Session

from core import needs_session
from general import schema, model


class UserRepository:
    @classmethod
    @needs_session
    def get_all_users(cls, session: Session):
        db_users: Sequence[schema.User] = session.query(schema.User).all()
        return [user.to_model() for user in db_users]

    @classmethod
    @needs_session
    def get_with_username(cls, username: str, session: Session):
        db_user: schema.User = session.query(schema.User).filter(
            schema.User.username == username
        ).one_or_none()
        if db_user:
            return db_user.to_model(with_password=True)
        else:
            return None

    @classmethod
    @needs_session
    def get_with_id(cls, id_: int, session: Session):
        db_user: schema.User = session.query(schema.User).get(id_)
        if db_user:
            return db_user.to_model(with_password=True)
        else:
            return None

    @classmethod
    @needs_session
    def upsert(cls, user: model.User, session: Session):
        db_user = session.query(schema.User).get(user.id)
        if not db_user:
            db_user = schema.User()
            session.add(db_user)

        db_user.username = user.username

        session.flush()
        return db_user.to_model()
