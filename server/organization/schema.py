
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from core import Role as auth_role
from curriculum import schema as curriculum_schema, model as curriculum_model
from general import model as general_model
from general.schema import BaseModel, User, Role
from organization import model


class Class(BaseModel):
    __tablename__ = 'class'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))

    def to_model(self, with_students=False, with_courses=False) -> model.Class:
        result = model.Class(
            id=self.id,
            name=self.name
        )
        if with_students:
            result.students = [student_ref.user.to_model() for student_ref in self.student_user_refs]
        if with_courses:
            result.course_list = [
                course_ref.course.to_model()
                for course_ref in self.course_refs
            ]
        return result


class ClassCourse(BaseModel):
    __tablename__ = 'class_course'
    id = sa.Column(sa.Integer, primary_key=True)

    class_id = sa.Column(sa.Integer, sa.ForeignKey(Class.id))
    cls = relationship(Class, backref='course_refs')

    course_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_schema.Course.id))
    course = relationship(curriculum_schema.Course, backref='class_refs')


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


class LessonClass(BaseModel):
    __tablename__ = 'lesson_class'
    id = sa.Column(sa.Integer, primary_key=True)
    is_visible = sa.Column(sa.Integer, nullable=False)

    lesson_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_schema.Lesson.id))
    lesson = relationship(curriculum_schema.Lesson, backref='class_refs')

    class_id = sa.Column(sa.Integer, sa.ForeignKey(Class.id))
    cls = relationship(Class, backref='lesson_refs')


class School(BaseModel):
    __tablename__ = 'school'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(400))

    def to_model(self, with_courses=False, with_teachers=False) -> model.School:
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
        if with_teachers:
            result.teachers = [
                general_model.User(
                    id=user_ref.user.id,
                    first_name=user_ref.user.first_name,
                    last_name=user_ref.user.last_name,
                    email=user_ref.user.email
                )
                for user_ref in self.user_refs
                if any([role_ref.role.name == str(auth_role.TEACHER) for role_ref in user_ref.user.role_refs])
            ]

        return result


class SchoolCourse(BaseModel):
    __tablename__ = 'school_course'
    id = sa.Column(sa.Integer, primary_key=True)

    school_id = sa.Column(sa.Integer, sa.ForeignKey(School.id))
    school = relationship(School, backref='course_refs')

    course_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_schema.Course.id))
    course = relationship(curriculum_schema.Course, backref='school_refs')


class SchoolUser(BaseModel):
    __tablename__ = 'school_user'
    id = sa.Column(sa.Integer, primary_key=True)

    school_id = sa.Column(sa.Integer, sa.ForeignKey(School.id))
    school = relationship(School, backref='user_refs')

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    user = relationship(User, backref='school_refs')
