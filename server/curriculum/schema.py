
import sqlalchemy as sa
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from curriculum import model
from general.schema import BaseModel, User


class Course(BaseModel):
    __tablename__ = 'course'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))

    author_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    author = relationship(User, backref='authored_courses')

    units = relationship('Unit', back_populates='course',
                         order_by='Unit.position', collection_class=ordering_list('position'))

    def to_model(self, with_units=False) -> model.Course:
        result = model.Course(
            id=self.id,
            name=self.name
        )
        if with_units:
            result.units = [unit.to_model() for unit in self.units]
        return result


class Unit(BaseModel):
    __tablename__ = 'unit'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))
    position = sa.Column(sa.Integer)

    course_id = sa.Column(sa.Integer, sa.ForeignKey(Course.id))
    course = relationship(Course, back_populates='units')

    lessons = relationship('Lesson', back_populates='unit',
                           order_by='Lesson.position', collection_class=ordering_list('position'))

    def to_model(self, with_lessons=False):
        result = model.Unit(
            id=self.id,
            name=self.name
        )
        if with_lessons:
            result.lessons = [lesson.to_model() for lesson in self.lessons]

        return result

    # TODO: Course <-> Unit will at least need to be a many-to-many at the start.
    #  Should Lessons, pages, sections, be too?


class Lesson(BaseModel):
    __tablename__ = 'lesson'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))
    position = sa.Column(sa.Integer)

    unit_id = sa.Column(sa.Integer, sa.ForeignKey(Unit.id))
    unit = relationship(Unit, back_populates='lessons')

    pages = relationship('Page', back_populates='lesson',
                         order_by='Page.position', collection_class=ordering_list('position'))

    def to_model(self, with_pages=False):
        result = model.Lesson(
            id=self.id,
            name=self.name
        )
        if with_pages:
            result.pages = [page.to_model() for page in self.pages]
        return result


class Page(BaseModel):
    """Division of sections with in a lesson, like 'intro' and maybe a small quiz at the end"""
    __tablename__ = 'page'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))
    html = sa.Column(sa.String(2000))
    position = sa.Column(sa.Integer)
    # TODO: order within a lesson

    lesson_id = sa.Column(sa.Integer, sa.ForeignKey(Lesson.id))
    lesson = relationship(Lesson, back_populates='pages')

    def to_model(self):
        result = model.Page(
            id=self.id,
            name=self.name,
            html=self.html
        )
        return result


class Question(BaseModel):
    """A place within a lesson's page that the student can provide a response"""
    __tablename__ = 'question'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.Enum(model.QuestionType))

    page_id = sa.Column(sa.Integer, sa.ForeignKey(Page.id))
    page = relationship(Page, backref='questions')

    def to_model(self) -> model.Question:
        result = model.Question(
            id=self.id,
            type=self.type,
            options=[option.to_model() for option in self.options]
        )
        return result


class Option(BaseModel):
    """Possible options to be selected for a question"""
    __tablename__ = 'option'
    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String(2000))

    question_id = sa.Column(sa.Integer, sa.ForeignKey(Question.id))
    question = relationship(Question, backref='options')

    def to_model(self) -> model.Option:
        result = model.Option(
            id=self.id,
            text=self.text
        )
        return result
