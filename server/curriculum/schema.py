from typing import List

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

    unit_refs: List['CourseUnit'] = relationship(
        'CourseUnit',
        back_populates='course',
        order_by='CourseUnit.position',
        collection_class=ordering_list('position')
    )

    def to_model(self, with_units=False) -> model.Course:
        result = model.Course(
            id=self.id,
            name=self.name
        )
        if with_units:
            result.units = [ref.unit.to_model(with_resources=True) for ref in self.unit_refs]
        return result


class CourseUnit(BaseModel):
    __tablename__ = 'course_unit'
    id = sa.Column(sa.Integer, primary_key=True)
    position = sa.Column(sa.Integer)

    course_id = sa.Column(sa.Integer, sa.ForeignKey(Course.id))
    course = relationship(Course, back_populates='unit_refs')

    unit_id = sa.Column(sa.Integer, sa.ForeignKey('unit.id'))
    unit = relationship('Unit', backref='course_refs')


class Unit(BaseModel):
    __tablename__ = 'unit'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))
    published = sa.Column(sa.Boolean, default=False)

    lessons: List['Lesson'] = relationship('Lesson', back_populates='unit',
                           order_by='Lesson.position', collection_class=ordering_list('position'))

    resource_refs: List['UnitResource'] = relationship('UnitResource', back_populates='unit')

    def to_model(self, with_lessons=False, with_resources=False):
        result = model.Unit(
            id=self.id,
            name=self.name
        )
        if with_lessons:
            result.lessons = [lesson.to_model(with_resources=True) for lesson in self.lessons]
        if with_resources:
            result.resources = [resource_ref.resource.to_model() for resource_ref in self.resource_refs]

        return result


class Lesson(BaseModel):
    __tablename__ = 'lesson'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))
    position = sa.Column(sa.Integer)

    unit_id = sa.Column(sa.Integer, sa.ForeignKey(Unit.id))
    unit = relationship(Unit, back_populates='lessons')

    pages = relationship('Page', back_populates='lesson',
                         order_by='Page.position', collection_class=ordering_list('position'))

    resource_refs: List['LessonResource'] = relationship('LessonResource', back_populates='lesson')

    def to_model(self, with_pages=False, with_resources=False):
        result = model.Lesson(
            id=self.id,
            name=self.name
        )
        if with_pages:
            result.pages = [page.to_model() for page in self.pages]
        if with_resources:
            result.resources = [resource_ref.resource.to_model() for resource_ref in self.resource_refs]
        return result


class Page(BaseModel):
    """Division of sections with in a lesson, like 'intro' and maybe a small quiz at the end"""
    __tablename__ = 'page'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200))
    html = sa.Column(sa.String(8000))
    position = sa.Column(sa.Integer)

    lesson_id = sa.Column(sa.Integer, sa.ForeignKey(Lesson.id))
    lesson = relationship(Lesson, back_populates='pages')

    def to_model(self):
        result = model.Page(
            id=self.id,
            name=self.name,
            html=self.html,
            position=self.position
        )
        return result


class Question(BaseModel):
    """A place within a lesson's page that the student can provide a response"""
    __tablename__ = 'question'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.Enum(model.QuestionType))

    page_id = sa.Column(sa.Integer, sa.ForeignKey(Page.id))
    page = relationship(Page, backref='questions')

    rubric_items = relationship('RubricItem', back_populates='question',
                                order_by='RubricItem.position', collection_class=ordering_list('position'))

    def to_model(self) -> model.Question:
        result = model.Question(
            id=self.id,
            type=self.type,
            options=[option.to_model() for option in self.options],
            rubric_items=[item.to_model() for item in self.rubric_items]
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


class RubricItem(BaseModel):
    """Grade-able item for a rubric"""
    __tablename__ = 'rubric_item'
    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String(1000))
    points = sa.Column(sa.Integer)
    position = sa.Column(sa.Integer)

    question_id = sa.Column(sa.Integer, sa.ForeignKey(Question.id))
    question = relationship(Question, back_populates='rubric_items')

    def to_model(self) -> model.RubricItem:
        result = model.RubricItem(
            id=self.id,
            text=self.text,
            points=self.points
        )
        return result


class Resource(BaseModel):
    """Link to external resource for teachers"""
    __tablename__ = 'resource'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(300))
    link = sa.Column(sa.String(500))

    def to_model(self) -> model.Resource:
        return model.Resource(
            id=self.id,
            name=self.name,
            link=self.link
        )


class UnitResource(BaseModel):
    __tablename__ = 'unit_resource'
    id = sa.Column(sa.Integer, primary_key=True)

    unit_id = sa.Column(sa.Integer, sa.ForeignKey(Unit.id))
    unit = relationship(Unit, back_populates='resource_refs')

    resource_id = sa.Column(sa.Integer, sa.ForeignKey(Resource.id))
    resource = relationship(Resource, backref='unit_refs')


class LessonResource(BaseModel):
    __tablename__ = 'lesson_resource'
    id = sa.Column(sa.Integer, primary_key=True)

    lesson_id = sa.Column(sa.Integer, sa.ForeignKey(Lesson.id))
    lesson = relationship(Lesson, back_populates='resource_refs')

    resource_id = sa.Column(sa.Integer, sa.ForeignKey(Resource.id))
    resource: Resource = relationship(Resource, backref='lesson_refs')
