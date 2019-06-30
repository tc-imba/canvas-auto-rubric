# Canvas Auto Rubric

## Installation

```bash
pip install git+https://github.com/tc-imba/canvas-auto-rubric.git@master
```


## Usage

```bash
Usage: canvasautorubric [OPTIONS]

Options:
  -u, --api-url TEXT        The Canvas LMS API URL.  [default:
                            https://umjicanvas.com/]
  -k, --api-key TEXT        The Canvas LMS API KEY.  [required]
  -c, --course-id TEXT      The Course ID of the target.  [required]
  -a, --assignment-id TEXT  The Assignment ID of the target.  [required]
  -r, --rubric-id TEXT      The Rubric ID of the target.
  -i, --input FILENAME      CSV file with grades.  [required]
  --no-sum                  Use the last row of the grade file as the total
                            grade.
  -h, --help                Show this message and exit.
  --version                 Show the version and exit.
```

## Input File Format

There is a `sample.csv`, of the data
```bash
3076,67.5,57.857,9,66.857
2337,69,57.294,8,65.294
2331,69,58.811,6,64.811
2743,67.5,54.427,10,64.427
584,70.5,56.272,8,64.272
3080,64.5,55.107,9,64.107
2983,70.5,56.272,5,61.272
2977,66,50.739,10,60.739
2693,60,52.126,8,60.126
3119,66,50.276,8,58.276
2808,66,51.94,6,57.94
2286,0,0,0,0
2649,0,0,0,0
```

The first column is the canvas uid, which can be found in the csv file exported from the `grades` page.

The rest columns are the grades in the order of which the rubric defines.

The total grade of one student is the sum of these columns. If the `--no-sum` argument is passed, the last column will be the total grade instead.

## Licence

Apache 2.0

## Dependencies

+ click
+ canvasapi
