import csv

import pbr.version
from canvasapi import Canvas
import click


def get_version():
    return pbr.version.VersionInfo('canvasautorubric')


def generate_rubric_assessment(rubric_criteria, grades):
    rubric_assessment = {}
    for i in range(len(rubric_criteria)):
        rubric_assessment[rubric_criteria[i]] = {'points': grades[i]}
    return rubric_assessment


def update_grade(assignment, rubric_criteria, uid, grade, grades):
    # print(uid, grade, grades)
    submission = assignment.get_submission(uid)
    data = {
        'submission': {
            'posted_grade': grade
        },
    }
    if rubric_criteria:
        data['rubric_assessment'] = generate_rubric_assessment(rubric_criteria, grades)
    submission.edit(**data)
    print('Updated:', uid, grade, grades)
    return uid


@click.command()
@click.option('-u', '--api-url', default='https://umjicanvas.com/', show_default=True, help='The Canvas LMS API URL.')
@click.option('-k', '--api-key', required=True, help='The Canvas LMS API KEY.')
@click.option('-c', '--course-id', required=True, help='The Course ID of the target.')
@click.option('-a', '--assignment-id', required=True, help='The Assignment ID of the target.')
@click.option('-r', '--rubric-id', help='The Rubric ID of the target.')
@click.option('-i', '--input', required=True, type=click.File(), help='CSV file with grades.')
@click.option('--no-sum', is_flag=True, help='Use the last row of the grade file as the total grade.')
@click.help_option('-h', '--help')
@click.version_option(version=get_version())
def main(api_url, api_key, course_id, assignment_id, rubric_id, input, no_sum):
    canvas = Canvas(api_url, api_key)
    course = canvas.get_course(course_id)
    print('Course:', course)
    assignment = course.get_assignment(assignment_id)
    print('Assignment:', assignment)
    rubric_criteria = None
    if rubric_id:
        rubric = course.get_rubric(rubric_id)
        print('Rubric:', rubric)
        rubric_detail = None
        if 'data' in rubric.__dict__:
            rubric_detail = rubric.data
        else:
            rubric_with_assessments = course.get_rubric(rubric_id, include='assessments', style='full')
            if 'assessments' in rubric_with_assessments.__dict__:
                rubric_detail = rubric_with_assessments.assessments[0]['data']
        if rubric_detail:
            rubric_criteria = [x['criterion_id'] for x in rubric_detail]
            print('Rubric Criteria:', rubric_criteria)
        else:
            print('Fetch Rubric data failed.')
            rubric_criteria = None

    reader = csv.reader(input)
    for row in reader:
        uid = row[0]
        grades = row[1:]
        if no_sum:
            grade = grades[-1]
        else:
            grade = sum(map(float, grades))
        update_grade(assignment, rubric_criteria, uid, grade, grades)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
