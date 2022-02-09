
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from curriculum import models as curriculum_models
from general import models as general_models


class Answer(curriculum_models.BaseModel):  # TODO: there's gotta be a better way to handle the BaseModel
    __tablename__ = 'answer'
    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String(2000))

    user_id = sa.Column(sa.Integer, sa.ForeignKey(general_models.User.id))
    user = relationship(general_models.User, backref='answers')

    question_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_models.Question.id))
    question = relationship(curriculum_models.Question, backref='answers')


class AnswerOption(curriculum_models.BaseModel):
    __tablename__ = 'answer_option'
    id = sa.Column(sa.Integer, primary_key=True)

    answer_id = sa.Column(sa.Integer, sa.ForeignKey(Answer.id))
    answer = relationship(Answer, backref='option_refs')

    option_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_models.Option.id))
    question = relationship(curriculum_models.Option, backref='answer_refs')
