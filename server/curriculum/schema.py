from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from general.schema import BaseModel


class Course(BaseModel):
    __tablename__ = 'course'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))


class Unit(BaseModel):
    __tablename__ = 'unit'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))

    course_id = sa.Column(sa.Integer, sa.ForeignKey(Course.id))
    course = relationship(Course, backref='units')

    # TODO: Course <-> Unit will atleast need to be a many-to-many at the start.
    #  Should Lessons, pages, sections, be too?


class Lesson(BaseModel):
    __tablename__ = 'lesson'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))

    unit_id = sa.Column(sa.Integer, sa.ForeignKey(Unit.id))
    unit = relationship(Unit, backref='lessons')


class Page(BaseModel):
    """Division of sections with in a lesson, like 'intro' and maybe a small quiz at the end"""
    __tablename__ = 'page'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))
    html = sa.Column(sa.String(2000))
    # TODO: order within a lesson

    lesson_id = sa.Column(sa.Integer, sa.ForeignKey(Lesson.id))
    lesson = relationship(Lesson, backref='pages')


class QuestionType(Enum):
    INLINE_TEXT = 1
    INLINE_DROPDOWN = 2
    PARAGRAPH = 3
    CHOICE = 4


class Question(BaseModel):
    """A place within a lesson's page that the student can provide a response"""
    __tablename__ = 'question'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.Enum(QuestionType))

    page_id = sa.Column(sa.Integer, sa.ForeignKey(Page.id))
    page = relationship(Page, backref='questions')


class Option(BaseModel):
    """Possible options to be selected for a question"""
    __tablename__ = 'option'
    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String(2000))

    question_id = sa.Column(sa.Integer, sa.ForeignKey(Question.id))
    question = relationship(Question, backref='options')
