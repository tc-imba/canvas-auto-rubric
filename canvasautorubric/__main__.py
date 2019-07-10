import csv
import datetime

import pbr.version
from canvasapi import Canvas
import click


def get_version():
    return pbr.version.VersionInfo('canvasautorubric')


def generate_rubric_assessment(rubric_criteria, rubric_description, grades):
    rubric_assessment = {}
    for i in range(len(rubric_criteria)):
        rubric_assessment[rubric_criteria[i]] = {'points': float(grades[i])}
        if rubric_description:
            rubric_assessment[rubric_criteria[i]]['comments'] = rubric_description[i]
    return rubric_assessment


def rubric_assessment_is_modified(assessment1, assessment2):
    if assessment1.keys() != assessment2.keys():
        return True
    for key in assessment1.keys():
        if assessment1[key]['points'] != assessment2[key]['points']:
            return True
        if assessment1[key]['comments'] != assessment2[key]['comments']:
            return True
    return False


def update_grade(assignment, uid, grade, grades, rubric_criteria, rubric_description):
    # print(uid, grade, grades)
    submission = assignment.get_submission(uid, include='rubric_assessment')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'comment': {
            'text_comment': '%s: Updated by canvas-auto-rubric (https://github.com/tc-imba/canvas-auto-rubric)' % now
        },
        'submission': {
            'posted_grade': grade
        },
    }
    if rubric_criteria:
        data['rubric_assessment'] = generate_rubric_assessment(grades=grades,
                                                               rubric_criteria=rubric_criteria,
                                                               rubric_description=rubric_description)
    # print(data)
    if rubric_assessment_is_modified(submission.rubric_assessment, data['rubric_assessment']):
        submission.edit(**data)
        print('Updated:', uid, grade, grades)
    else:
        print('Not Modified:', uid)
    return uid


@click.command()
@click.option('-u', '--api-url', default='https://umjicanvas.com/', show_default=True, help='The Canvas LMS API URL.')
@click.option('-k', '--api-key', required=True, help='The Canvas LMS API KEY.')
@click.option('-c', '--course-id', required=True, help='The Course ID of the target.')
@click.option('-a', '--assignment-id', required=True, help='The Assignment ID of the target.')
@click.option('-r', '--rubric-id', help='The Rubric ID of the target.')
@click.option('-i', '--input', required=True, type=click.File(), help='CSV file with grades.')
@click.option('--no-sum', is_flag=True, help='Use the last row of the grade file as the total grade.')
@click.option('--header', is_flag=True, help='Use the first row of the grade file as description.')
@click.help_option('-h', '--help')
@click.version_option(version=get_version())
def main(api_url, api_key, course_id, assignment_id, rubric_id, input, no_sum, header):
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
    rubric_description = None
    for row in reader:
        if header:
            rubric_description = row[1:]
            header = False
            continue
        uid = row[0]
        grades = row[1:]
        if no_sum:
            grade = grades[-1]
        else:
            grade = sum(map(float, grades))
        update_grade(assignment=assignment, uid=uid, grade=grade, grades=grades,
                     rubric_criteria=rubric_criteria, rubric_description=rubric_description)
        # break


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
