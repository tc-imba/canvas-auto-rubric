# Import the Canvas class
from canvasapi import Canvas
from pprint import pprint
import csv
import multiprocessing
import time

# Canvas API URL
API_URL = "https://umjicanvas.com/"
# Canvas API key
API_KEY = ""

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

course = canvas.get_course(1091)
print(course)

assignment = course.get_assignment(8959)
print(assignment)

# submission = assignment.get_submission(2936)
# print(submission.attributes)

rubric = course.get_rubric(231, include='assessments', style='full')
if rubric.assessments:
    rubric_detail = rubric.assessments[0]['data']
    rubric_list = [x['criterion_id'] for x in rubric_detail]
else:
    assert 0


def generate_rubric_assessment(grades):
    rubric_assessment = {}
    for i in range(len(rubric_list)):
        rubric_assessment[rubric_list[i]] = {'points': grades[i]}
    return rubric_assessment


def update_grade(uid, grade, grades):
    # print(uid, grade, grades)
    submission = assignment.get_submission(uid)
    data = {
        'submission': {
            'posted_grade': grade
        },
        'rubric_assessment': generate_rubric_assessment(grades)
    }
    submission.edit(**data)
    print(uid, grade, grades)
    return uid


# update_grade(2952, 100, ['90', '90', '10', '100'])

jobs = multiprocessing.cpu_count()
# jobs = 2

grades_dict = {}

with open('p2_curved_clean.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        grades_dict[row[0]] = row
        # update_grade(row[0], row[-1], row[1:])

#
# results = []
# pool = multiprocessing.Pool(processes=jobs)
# for row in grades_dict.values():
#     results.append(pool.apply_async(update_grade, (row[0], row[-1], row[1:],)))
# pool.close()
# pool.join()
# for result in results:
#     del grades_dict[result.get()]


for row in grades_dict.values():
    update_grade(row[0], row[-1], row[1:])

