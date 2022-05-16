
from werkzeug.exceptions import Forbidden

from curriculum import model as curriculum_models, repository as curriculum_repository
from responses import repository as responses_repository, model


def answer_provided(user_id: int, question_id: int, submitted: bool, answer):
    # TODO: should have a db lock on this to prevent multiple requests from being processed at the same time for a given
    #  user's answers

    answer_model = model.Answer(
        user_id=user_id,
        question_id=question_id,
        locked=submitted,
        submitted=submitted
    )

    existing_answer = responses_repository.AnswerRepository.find_existing(answer_model)
    if existing_answer and existing_answer.locked:
        raise Forbidden('Answer is submitted and locked')

    question = curriculum_repository.QuestionRepository.get(question_id)
    if question.type in [
        curriculum_models.QuestionType.PARAGRAPH,
        curriculum_models.QuestionType.INLINE_TEXT,
        curriculum_models.QuestionType.RUBRIC
    ]:
        answer_model.text = answer
    else:
        answer_model.selected_option_ids = answer

    return responses_repository.AnswerRepository.upsert(answer_model)


def rubric_item_graded(answer_id, rubric_item_id, grade) -> model.RubricGrade:
    rubric_grade = model.RubricGrade(
        rubric_item_id=rubric_item_id,
        grade=grade
    )
    return responses_repository.RubricGradeRepository.upsert(
        rubric_grade=rubric_grade,
        answer_id=answer_id
    )
