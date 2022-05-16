
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from curriculum import schema as curriculum_schema, model as curriculum_model
from general.schema import BaseModel, User
from organization import model


class Class(BaseModel):
    __tablename__ = 'class'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))

    def to_model(self, with_students=False) -> model.Class:
        result = model.Class(
            id=self.id,
            name=self.name
        )
        if with_students:
            result.students = [student_ref.user.to_model() for student_ref in self.student_user_refs]
        return result


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


class School(BaseModel):
    __tablename__ = 'school'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(400))

    def to_model(self, with_courses=False) -> model.School:
        result = model.School(
            id=self.id,
            name=self.name
        )
        if with_courses:
            result.courses = [
                curriculum_model.Course(
                    id=course_ref.course.id,
                    name=course_ref.course.name
                )
                for course_ref in self.course_refs
            ]

        return result


class SchoolCourse(BaseModel):
    __tablename__ = 'school_course'
    id = sa.Column(sa.Integer, primary_key=True)

    school_id = sa.Column(sa.Integer, sa.ForeignKey(School.id))
    school = relationship(School, backref='course_refs')

    course_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_schema.Course.id))
    course = relationship(curriculum_schema.Course, backref='school_refs')
