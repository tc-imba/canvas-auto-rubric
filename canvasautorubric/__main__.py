import datetime
import math
import enlighten

from canvasautorubric import utils
from canvasapi import Canvas
from canvasapi.exceptions import CanvasException
import click
import logzero
from logzero import logger

LOGGER_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s canvasautorubric:%(lineno)d]%(end_color)s %(message)s'
formatter = logzero.LogFormatter(fmt=LOGGER_FORMAT)
logzero.setup_default_logger(formatter=formatter)


def parse_grade(grade_str):
    try:
        grade = float(grade_str)
        if not math.isnan(grade):
            return grade
    except:
        pass
    return 0


def generate_rubric_assessment(rubric_criteria, rubric_description, grades):
    rubric_assessment = {}
    for i in range(len(rubric_criteria)):
        rubric_assessment[rubric_criteria[i]] = {'points': parse_grade(grades[i])}
        if rubric_description:
            rubric_assessment[rubric_criteria[i]]['comments'] = rubric_description[i]
    return rubric_assessment


def rubric_assessment_is_modified(assessment1, assessment2):
    if assessment1.keys() != assessment2.keys():
        return True
    for key in assessment1.keys():
        if assessment1[key].get('points', None) != assessment2[key].get('points', None):
            return True
        if assessment1[key].get('comments', None) != assessment2[key].get('comments', None):
            return True
    return False


def get_grade_float(grade):
    try:
        return float(grade)
    except:
        return 0


def update_grade(assignment, uid, grade, grades, rubric_criteria, rubric_description, no_comment, dry_run):
    # print(uid, grade, grades)
    submission = assignment.get_submission(uid, include='rubric_assessment')
    # pprint(submission)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'submission': {
            'posted_grade': grade
        },
    }
    if not no_comment:
        data['comment'] = {
            'text_comment': '%s: Updated by canvas-auto-rubric (https://github.com/tc-imba/canvas-auto-rubric)' % now
        }
    new_rubric_assessment = None
    if rubric_criteria:
        new_rubric_assessment = generate_rubric_assessment(grades=grades,
                                                           rubric_criteria=rubric_criteria,
                                                           rubric_description=rubric_description)
    # print(data)
    if new_rubric_assessment and (not hasattr(submission, 'rubric_assessment') or
                                  rubric_assessment_is_modified(submission.rubric_assessment, new_rubric_assessment)):
        data['rubric_assessment'] = new_rubric_assessment
        if not dry_run:
            submission.edit(**data)
        logger.info('Updated Rubric: %s %s %s', uid, grade, grades)
    elif hasattr(submission, 'grade') and get_grade_float(submission.grade) == grade:
        logger.info('Not Modified: %s', uid)
    else:
        if not dry_run:
            submission.edit(**data)
        logger.info('Updated Grade: %s %s %s', uid, grade, grades)
    return uid


def get_rubric_criteria(course, rubric_id):
    rubric_criteria = None
    if rubric_id:
        rubric = course.get_rubric(rubric_id)
        logger.info('Rubric: %s', rubric)
        rubric_detail = None
        if 'data' in rubric.__dict__:
            rubric_detail = rubric.data
        else:
            rubric_with_assessments = course.get_rubric(rubric_id, include='assessments', style='full')
            # pprint(rubric_with_assessments)
            if hasattr(rubric_with_assessments, 'assessments'):
                rubric_detail = rubric_with_assessments.assessments[0]['data']
        if rubric_detail:
            rubric_criteria = [x['criterion_id'] for x in rubric_detail]
            logger.info('Rubric Criteria: %s', rubric_criteria)
        else:
            logger.warning('Fetch Rubric data failed.')
            rubric_criteria = None
    return rubric_criteria


@click.command()
@click.option('-u', '--api-url', default='https://umjicanvas.com/', show_default=True, help='The Canvas LMS API URL.')
@click.option('-k', '--api-key', required=True, help='The Canvas LMS API KEY.')
@click.option('-c', '--course-id', required=True, help='The Course ID of the target.')
@click.option('-a', '--assignment-id', required=True, help='The Assignment ID of the target.')
@click.option('-r', '--rubric-id', help='The Rubric ID of the target.')
@click.option('-i', '--input-file', required=True, type=click.Path(exists=True), help='CSV/XLS(X) file with grades.')
@click.option('--sheet', default=0, show_default=True, help='The sheet id in XLS(X) file')
@click.option('--no-sum', is_flag=True, help='Use the last row of the grade file as the total grade.')
@click.option('--header', is_flag=True, help='Use the first row of the grade file as description.')
@click.option('--no-comment', is_flag=True, help='Do not add a update comment in the submission comments.')
@click.option('--debug', is_flag=True, help='Debug mode.')
@click.option('--dry-run', is_flag=True,
              help='Nothing is actually updated, the actions to be performed are written to the terminal.')
@click.help_option('-h', '--help')
@click.version_option(version=utils.get_version())
def main(api_url, api_key, course_id, assignment_id, rubric_id, input_file,
         sheet, no_sum, header, no_comment, debug, dry_run):
    logger.info('Canvas Auto Rubric: version %s', utils.get_version())
    canvas = Canvas(api_url, api_key)
    course = canvas.get_course(course_id)
    logger.info('Course: %s', course)
    assignment = course.get_assignment(assignment_id)
    logger.info('Assignment: %s', assignment)
    rubric_criteria = get_rubric_criteria(course, rubric_id)
    if rubric_id and rubric_criteria is None:
        logger.error('Please open speedgrader and set a score with Rubric for any student!')
        logger.error('%s/courses/%d/gradebook/speed_grader?assignment_id=%d', api_url, course.id, assignment.id)
        exit(1)
    if no_sum:
        logger.info('Use the last row of the grade file as the total grade. (--no-sum)')
    if header:
        logger.info('Use the first row of the grade file as description. (--header)')
    if no_comment:
        logger.info('Do not add a update comment in the submission comments. (--no-comment)')
    if dry_run:
        logger.warn('Nothing is actually updated, the actions to be performed are written to the terminal. (--dry-run)')

    df = utils.read_data(input_file, header, sheet)
    if header:
        rubric_description = df.columns.tolist()
    else:
        rubric_description = None

    manager = enlighten.get_manager()
    pbar = manager.counter(total=len(df), desc='Progress', unit='ticks')
    for uid, row in df.iterrows():
        try:
            grades = list(map(parse_grade, row.tolist()))
            if no_sum:
                grade = grades[-1]
                grades = grades[:-1]
            else:
                grade = sum(grades)
            update_grade(assignment=assignment, uid=uid, grade=grade, grades=grades,
                         rubric_criteria=rubric_criteria, rubric_description=rubric_description,
                         no_comment=no_comment, dry_run=dry_run)
        except Exception as e:
            logger.error('Error: %s %s', uid, str(e))
            if debug:
                logger.exception(e)
        pbar.update()


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
