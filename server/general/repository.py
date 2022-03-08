from typing import Sequence

from sqlalchemy.orm import joinedload, Session, Query

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
    def get_with_username(cls, username: str, session: Session, populate_roles=False):
        user_query = cls._build_user_query(session=session, with_roles=populate_roles)
        db_user: schema.User = user_query.filter(
            schema.User.username == username
        ).one_or_none()
        if db_user:
            return db_user.to_model(with_password=True, with_roles=True)
        else:
            return None

    @classmethod
    @needs_session
    def get_with_id(cls, id_: int, session: Session, populate_roles=False):
        user_query = cls._build_user_query(session=session, with_roles=populate_roles)
        db_user: schema.User = user_query.get(id_)
        if db_user:
            return db_user.to_model(with_password=True, with_roles=True)
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

    @classmethod
    def _build_user_query(cls, session: Session, with_roles=False):
        user_query = session.query(schema.User)
        if with_roles:
            user_query = user_query.options(
                joinedload(schema.User.role_refs).joinedload(schema.UserRole.role)
            )
        return user_query
