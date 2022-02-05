
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseModel = declarative_base()


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
    # TODO: order within a lesson

    lesson_id = sa.Column(sa.Integer, sa.ForeignKey(Lesson.id))

    relationship(Lesson, backref='pages')


class Section(BaseModel):
    """
    Semi-atomic unit of a lesson (can still be composed of other elements).
    Sections would be grouped within a page of a lesson and shown in order, but can contain
    flexible layouts of sub-elements.
    """
    __tablename__ = 'section'
    id = sa.Column(sa.Integer, primary_key=True)
    text_html = sa.Column(sa.String(2000))
    # TODO: order within a page
    #  want to be able to have sections that are just text, but also sections that contain single/multi
    #  select options that would be answered (OptionGroup objects that define their options and whether
    #  multiple can be clicked?), free-text fields for answering response_fields, etc...

    page_id = sa.Column(sa.Integer, sa.ForeignKey(Page.id))

    relationship(Page, backref='sections')
