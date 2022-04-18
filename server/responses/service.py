
from curriculum import model as curriculum_models, repository as curriculum_repository
from responses import repository as responses_repository, model


def answer_provided(user_id: int, question_id: int, answer):
    answer_model = model.Answer(
        user_id=user_id,
        question_id=question_id
    )
    question = curriculum_repository.QuestionRepository.get(question_id)
    if question.type in [
        curriculum_models.QuestionType.PARAGRAPH,
        curriculum_models.QuestionType.INLINE_TEXT,
        curriculum_models.QuestionType.RUBRIC
    ]:
        answer_model.text = answer
    else:
        answer_model.selected_option_ids = answer
    responses_repository.AnswerRepository.upsert(answer_model)

    return answer_model


def rubric_item_graded(answer_id, rubric_item_id, grade) -> model.RubricGrade:
    rubric_grade = model.RubricGrade(
        rubric_item_id=rubric_item_id,
        grade=grade
    )
    return responses_repository.RubricGradeRepository.upsert(
        rubric_grade=rubric_grade,
        answer_id=answer_id
    )
