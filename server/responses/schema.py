
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from curriculum import schema as curriculum_models
from general import schema as general_schema
from general.schema import BaseModel
from responses import model


class Answer(BaseModel):
    __tablename__ = 'answer'
    id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.String(2000))

    user_id = sa.Column(sa.Integer, sa.ForeignKey(general_schema.User.id))
    user = relationship(general_schema.User, backref='answers')

    question_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_models.Question.id))
    question = relationship(curriculum_models.Question, backref='answers')

    def to_model(self) -> model.Answer:
        result = model.Answer(
            id=self.id,
            user_id=self.user_id,
            question_id=self.question_id,
            text=self.text,
            selected_option_ids=[option_ref.option_id for option_ref in self.option_refs]
        )
        return result


class AnswerOption(BaseModel):
    __tablename__ = 'answer_option'
    id = sa.Column(sa.Integer, primary_key=True)

    answer_id = sa.Column(sa.Integer, sa.ForeignKey(Answer.id))
    answer = relationship(Answer, backref='option_refs')

    option_id = sa.Column(sa.Integer, sa.ForeignKey(curriculum_models.Option.id))
    question = relationship(curriculum_models.Option, backref='answer_refs')
