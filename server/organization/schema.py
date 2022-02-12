
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from general.schema import BaseModel, User


class Class(BaseModel):
    __tablename__ = 'class'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))


class TeacherClass(BaseModel):
    __tablename__ = 'teacher_class'
    id = sa.Column(sa.Integer, primary_key=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    user = relationship(User, backref='teaching_class_refs')

    class_id = sa.Column(sa.Integer, sa.ForeignKey(Class.id))
    cls = relationship(Class, backref='teaching_user_refs')


class StudentClass(BaseModel):
    __tablename__ = 'student_class'
    id = sa.Column(sa.Integer, primary_key=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    user = relationship(User, backref='student_class_refs')

    class_id = sa.Column(sa.Integer, sa.ForeignKey(Class.id))
    cls = relationship(Class, backref='student_user_refs')
