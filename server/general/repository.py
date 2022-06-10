from typing import Sequence

from sqlalchemy.orm import aliased, joinedload, Session, Query

from core import needs_session, Role
from general import schema, model
from organization import schema as organization_schema


class UserRepository:
    @classmethod
    @needs_session
    def get_all_users(cls, session: Session, role_filter=None, email_like_filter=None):
        query = session.query(schema.User)
        if role_filter:
            query = query.join(
                schema.UserRole,
                schema.User.id == schema.UserRole.user_id
            ).join(
                schema.Role,
                schema.Role.id == schema.UserRole.role_id
            ).filter(
                schema.Role.name == str(role_filter)
            )
        if email_like_filter:
            query = query.filter(
                schema.User.email.ilike(f'%{email_like_filter}%')
            )

        db_users: Sequence[schema.User] = query.all()
        return [user.to_model() for user in db_users]

    @classmethod
    @needs_session
    def get_students_in_school_with_teacher(cls, teacher_user_id, session: Session):
        student_school = aliased(organization_schema.SchoolUser)
        teacher_school = aliased(organization_schema.SchoolUser)
        query = session.query(
            schema.User
        ).join(
            schema.UserRole
        ).join(
            schema.Role
        ).join(
            student_school,
            student_school.user_id == schema.User.id
        ).join(
            teacher_school,
            teacher_school.school_id == student_school.school_id
        ).filter(
            teacher_school.user_id == teacher_user_id,
            schema.Role.name == 'student'
        )

        db_users: Sequence[schema.User] = query.all()
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
    def get_with_email(cls, email: str, session: Session, populate_roles=False):
        user_query = cls._build_user_query(session=session, with_roles=populate_roles)
        db_user: schema.User = user_query.filter(
            schema.User.email == email
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
            role_list = session.query(schema.Role).filter(
                schema.Role.name.in_(user.roles)
            )

            db_user.role_refs = [
                schema.UserRole(user=db_user, role=role)
                for role in role_list
            ]
            session.add(db_user)

        db_user.username = user.username
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.email = user.email

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
