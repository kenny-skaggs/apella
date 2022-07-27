from collections import defaultdict
import csv
import json
import logging
import os

from dotenv import load_dotenv
import typer

load_dotenv()

from curriculum import schema as curriculum_schema, model as curriculum_model, repository as curriculum_repository, html_processing
from general import schema as general_schema
from organization import schema as organization_schema
from tool_kit.external import DatabaseConnection

app = typer.Typer()

connection = DatabaseConnection(
    username=os.environ['PROD_DB_USERNAME'],
    password=os.environ['PROD_DB_PASSWORD'],
    port=os.environ['PROD_DB_PORT']
)


def _get_file_data(file_name):
    with open(f'./server/scripts/data/{file_name}') as file:
        return list(csv.DictReader(file))


def migrate_courses(session):
    """
    select course_id id, course_name name
    from course c;
    """
    for course in _get_file_data('courses.csv'):
        id = course['id']
        name = course['name']
        typer.echo(f'adding course "{name}')
        session.add(curriculum_schema.Course(
            id=id,
            name=name
        ))


def migrate_units(session):
    """
    select unit_id id, unit_name name, published
    from unit;
    """
    for unit in _get_file_data('unit.csv'):
        typer.echo(f'adding unit "{unit["name"]}"')
        session.add(curriculum_schema.Unit(
            id=unit['id'],
            name=unit['name'],
            published=unit['published'] == '1'
        ))


def migrate_course_units(session):
    """
    select *
    from course_unit cu ;
    """
    for course_unit in _get_file_data('course_unit.csv'):
        typer.echo(f'linking unit {course_unit["unit_id"]} and course {course_unit["course_id"]}')
        session.add(curriculum_schema.CourseUnit(
            id=course_unit['id'],
            unit_id=course_unit['unit_id'],
            course_id=course_unit['course_id'],
            position=course_unit['unit_order']
        ))


def migrate_unit_resources(session):
    """
    select * from unit_attachment ua;
    """
    for unit_resource in _get_file_data('unit_resource.csv'):
        typer.echo(f'adding resource "{unit_resource["name"]}" to unit {unit_resource["unit_id"]}')
        session.add(
            curriculum_schema.Resource(
                name=unit_resource['name'],
                link=unit_resource['url'],
                unit_refs=[
                    curriculum_schema.UnitResource(
                        unit_id=unit_resource['unit_id']
                    )
                ]
            )
        )


def migrate_lessons(session):
    """
    select s.section_id id, section_name name, section_order position, s.lesson_id, learn_content
    from `section` s
    inner join learn l on l.section_id = s.section_id
    inner join lesson l2 on l2.lesson_id = s.lesson_id and l2.active
    where section_type = 'learn' and section_active ;
    """
    for lesson in _get_file_data('lesson.csv'):
        typer.echo(f'adding lesson "{lesson["name"]}')
        session.add(
            curriculum_schema.Lesson(
                id=lesson['id'],
                name=lesson['name'],
                position=lesson['position'],
                unit_id=lesson['unit_id']
            )
        )


def migrate_lesson_resources(session):
    """
    select la.*
    from lesson_attachment la
    inner join lesson l on l.lesson_id = la.lesson_id
    where l.active ;
    """
    for lesson_resource in _get_file_data('lesson_resource.csv'):
        typer.echo(f'adding resource "{lesson_resource["name"]}" to lesson {lesson_resource["lesson_id"]}')
        session.add(
            curriculum_schema.Resource(
                name=lesson_resource['name'],
                link=lesson_resource['url'],
                lesson_refs=[
                    curriculum_schema.LessonResource(
                        lesson_id=lesson_resource['lesson_id']
                    )
                ]
            )
        )


def migrate_users(session):
    """
    select us.id, us.user_id, us.school_id
    from user_school us
    inner join `user` u on u.user_id = us.user_id and u.active
    inner join school s on s.school_id = us.school_id and s.hidden_pd_school = 0;
    """
    for user in _get_file_data('user.csv'):
        typer.echo(f'adding {user["id"]}')
        user_obj = general_schema.User(
            id=user['id'],
            email=user['email'] if user['email'] != '' else None,
            username=user['username'] if user['username'] != '' else None,
            password=user['password'] if user['password'] != '' else None,
            first_name=user['first_name'],
            last_name=user['last_name']
        )
        session.add(user_obj)

        role = user['privilege']
        if role == 'creator':
            user_obj.role_refs = [general_schema.UserRole(role_id=1)]
        elif role == 'student':
            user_obj.role_refs = [general_schema.UserRole(role_id=3)]
        elif role == 'teacher':
            user_obj.role_refs = [general_schema.UserRole(role_id=2)]
        elif role == 'admin':
            user_obj.role_refs = [general_schema.UserRole(role_id=4)]


def migrate_schools(session):
    """
    select school_id id, school_name name
    from school s
    where hidden_pd_school = 0;
    """
    for school in _get_file_data('school.csv'):
        typer.echo(f'adding school "{school["name"]}')
        session.add(
            organization_schema.School(
                id=school['id'],
                name=school['name']
            )
        )


def migrate_school_users(session):
    """
    select id, user_id, school_id
    from user_school us;
    """
    for school_user in _get_file_data('school_user.csv'):
        typer.echo(f'adding user {school_user["user_id"]} to school {school_user["school_id"]}')
        session.add(
            organization_schema.SchoolUser(
                id=school_user['id'],
                user_id=school_user['user_id'],
                school_id=school_user['school_id']
            )
        )


def migrate_school_courses(session):
    """
    select school_id, course_id
    from school_course sc
    where active;
    """
    for school_course in _get_file_data('school_course.csv'):
        typer.echo(f'linking {school_course["course_id"]} to school {school_course["school_id"]}')
        session.add(
            organization_schema.SchoolCourse(
                school_id=school_course['school_id'],
                course_id=school_course['course_id']
            )
        )


def migrate_classes(session):
    """
    select id, course_id, name, teacher_school_id user_school_id
    from class c
    where active and teacher_school_id is not null;
    """
    for cls in _get_file_data('class.csv'):
        # cls_obj = organization_schema.Class(
        #     id=cls['id'],
        #     name=cls['name']
        # )
        #
        # cls_obj.course_refs = [
        #     organization_schema.ClassCourse(course_id=cls['course_id'])
        # ]
        #
        # user_school = session.query(
        #     organization_schema.SchoolUser
        # ).filter(
        #     organization_schema.SchoolUser.id == cls['user_school_id']
        # ).one_or_none()
        # if user_school:
        #     typer.echo(f'adding class {cls["name"]}')
        #     cls_obj.teaching_user_refs = [
        #         organization_schema.TeacherClass(user_id=user_school.user_id)
        #     ]
        #     session.add(cls_obj)

        user_school = session.query(
            organization_schema.SchoolUser
        ).filter(
            organization_schema.SchoolUser.id == cls['user_school_id']
        ).one_or_none()
        if user_school:
            cls_obj = session.query(
                organization_schema.Class
            ).filter(
                organization_schema.Class.id == cls['id']
            ).one_or_none()
            if cls_obj:
                typer.echo(f'adding teacher for class {cls["name"]}')
                session.add(
                    organization_schema.TeacherClass(
                        user_id=user_school.user_id,
                        class_id=cls['id']
                    )
                )


def migrate_student_classes(session):
    """
    select id, class_id, user_id
    from student_class sc
    where active;
    """
    cls_map = {}
    for student_class in _get_file_data('student_class.csv'):
        class_id = student_class['class_id']
        if class_id not in cls_map:
            cls_map[class_id] = session.query(organization_schema.Class).filter(
                organization_schema.Class.id == class_id
            ).one_or_none()

        cls_obj = cls_map[class_id]
        if cls_obj:
            student_obj = session.query(general_schema.User).filter(
                general_schema.User.id == student_class['user_id']
            ).one_or_none()

            if student_obj:
                typer.echo(f'adding student {student_class["user_id"]} to class "{cls_obj.name}"')
                session.add(organization_schema.StudentClass(
                    id=student_class['id'],
                    user_id=student_class['user_id'],
                    class_id=class_id
                ))


def migrate_learns(session):
    """
    select s.section_id id, section_name name, section_order position, s.lesson_id, learn_content
    from `section` s
    inner join learn l on l.section_id = s.section_id
    inner join lesson l2 on l2.lesson_id = s.lesson_id and l2.active
    where section_type = 'learn' and section_active ;
    """
    for learn_data in _get_file_data('learn.csv'):
        session.add(
            curriculum_schema.Page(
                id=learn_data['id'],
                name=learn_data['name'],
                html=learn_data['learn_content'],
                position=learn_data['position'],
                lesson_id=learn_data['lesson_id']
            )
        )


def _get_html_for_question(cfu_data, cfu_id_option_list_map):
    # just the html for an OR cfu,
    # need to save each mc option and get the id, then build out the option list in the html for a
    # multiple choice question
    if cfu_data['type'] == 'or':
        return f"""
            <div>
                {cfu_data['question_html']}
                <p class="wysiwyg_question question_paragraph" contenteditable="false">
                    Student will have a large text box to enter text here.
                </p>
            </div>
        """
    elif cfu_data['type'] == 'mc':
        option_html_list = cfu_id_option_list_map[cfu_data['id']]
        options_text = [
            {"id": 0, "html": html.replace("'", '&#x27;')}
            for html in option_html_list
        ]
        return f"""
            <div>
                {cfu_data['question_html']}
                <p class="wysiwyg_question question_choice" contenteditable="false"
                    options='{json.dumps(options_text)}'>
                    Options for a multiple choice question will appear here
                </p>
            </div>
        """
    else:
        raise Exception(f'found a cfu with type "{cfu_data["type"]}"')


def migrate_cfus(session):
    """
    select mc_id id, mc_option option_html, cfu_id
    from mc_option mo
    order by cfu_id, mc_order;

    select cfu_id id, c.section_id, cfu_type type, cfu_content question_html, s.lesson_id lesson_id,
    s.section_name page_name, s.section_order page_position
    from `section` s
    inner join cfu c on c.section_id = s.section_id and section_active
    inner join lesson l on l.lesson_id = s.lesson_id and l.active
    where cfu_active
    order by
    section_id, -- check for existence of section id in apella, caching the result for later checks
    `sequence`;
    """
    cfu_id_option_list_map = defaultdict(list)
    for option_data in _get_file_data('option.csv'):
        cfu_id_option_list_map[option_data['cfu_id']].append(option_data['option_html'])

    page_blob_map = {}
    for cfu_data in _get_file_data('cfu.csv'):
        page = page_blob_map.get(cfu_data['section_id'])
        if page is None:
            page = {
                'id': cfu_data['section_id'],
                'name': cfu_data['page_name'],
                'position': cfu_data['page_position'],
                'lesson_id': cfu_data['lesson_id'],
                'question_list': [],
                'page_position': cfu_data['page_position']
            }
            page_blob_map[page['id']] = page

        page['question_list'].append(
            _get_html_for_question(
                cfu_data=cfu_data,
                cfu_id_option_list_map=cfu_id_option_list_map
            )
        )

    lesson_id_set = set()

    for page_blob in page_blob_map.values():
        typer.echo(f'storing page {page_blob["id"]}')
        page_model = curriculum_model.Page(
            id=page_blob['id'],
            name=page_blob['name'],
            lesson_id=page_blob['lesson_id'],
            html='<hr>'.join(page_blob['question_list']),
            position=page_blob['page_position']
        )

        # todo: process the html using the parser
        upsert_page = curriculum_repository.PageRepository.upsert(
            page=page_model,
            session=session
        )

        parser = html_processing.QuestionParser(page_id=upsert_page.id, session=session)
        upsert_page.html = parser.process_html(upsert_page.html)

        curriculum_repository.PageRepository.upsert(
            page=upsert_page,
            session=session,
            do_update=True
        )

        lesson_id_set.add(page_model.lesson_id)

    # for lesson_id in lesson_id_set:
    #     lesson = session.query(curriculum_schema.Lesson).filter(
    #         curriculum_schema.Lesson.id == lesson_id
    #     ).one_or_none()
    #     lesson.pages.reorder()


def migrate_rubrics(session):
    """
    SELECT s.section_id as id, section_name as name, section_order as position, s.lesson_id, r.description rubric_content, max_range points
    from rubric r
    inner join `section` s on s.section_id = r.section_id and s.section_type = 'rubric'
    inner join lesson l on s.lesson_id = l.lesson_id and l.active
    where s.section_active;

    select id, section_id page_id, description, weight_override points, `sequence` position
    from rubric_item ri
    where active;

    SELECT s.section_id as id, section_name as name, section_order as position, s.lesson_id, p.description rubric_content
    from project p
    inner join `section` s on s.section_id = p.section_id and s.section_type = 'proj'
    inner join lesson l on s.lesson_id = l.lesson_id and l.active
    where s.section_active;
    """
    rubric_item_lists = defaultdict(list)
    # for item_data in _get_file_data('rubric_item.csv'):
    #     rubric_item_lists[item_data['page_id']].append(
    #         curriculum_schema.RubricItem(
    #             id=item_data['id'],
    #             text=item_data['description'],
    #             points=item_data['points'] or None,
    #             position=item_data['position']
    #         )
    #     )

    for rubric_data in _get_file_data('rubric.csv'):
        rubric_page = curriculum_schema.Page(
            id=rubric_data['id'],
            name=rubric_data['name'],
            html=rubric_data['rubric_content'],
            position=rubric_data['position'],
            lesson_id=rubric_data['lesson_id']
        )
        session.add(rubric_page)

        rubric_items = rubric_item_lists[rubric_data['id']]
        rubric_question = curriculum_schema.Question(
            type=curriculum_model.QuestionType.RUBRIC,
            page=rubric_page,
            rubric_items=rubric_items
        )
        session.add(rubric_question)
        session.flush()

        item_list_json = json.dumps([
            {
                'id': item.id,
                'text': item.text,
                'points': item.points or rubric_data['points']
            }
            for item in rubric_items
        ]).replace("'", '&#x27;')
        rubric_page.html += f"""
        <div class="wysiwyg_question question_rubric" contenteditable="false"
            question_id="{rubric_question.id}" questionid="{rubric_question.id}"
            rubric_items='{item_list_json}'
        >
            A project rubric will appear here.
        </div>
        """


@app.command()
def migrate():
    typer.echo('Running migration...')
    with connection.get_new_session() as session:
        ...
        # migrate_courses(session)
        # migrate_units(session)
        # migrate_course_units(session)
        # migrate_unit_resources(session)
        # migrate_lessons(session)
        # migrate_lesson_resources(session)
        # migrate_users(session)
        # migrate_schools(session)
        # migrate_school_users(session)
        # migrate_school_courses(session)
        # migrate_classes(session)
        # migrate_student_classes(session)
        # migrate_learns(session)
        # migrate_cfus(session)
        migrate_rubrics(session)


if __name__ == '__main__':
    app()
