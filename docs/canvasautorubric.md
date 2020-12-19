# Usage

## Commands

```bash
Usage: canvasautorubric [OPTIONS]

Options:
  -u, --api-url TEXT        The Canvas LMS API URL.  [default:
                            https://umjicanvas.com/]

  -k, --api-key TEXT        The Canvas LMS API KEY.  [required]
  -c, --course-id TEXT      The Course ID of the target.  [required]
  -a, --assignment-id TEXT  The Assignment ID of the target.  [required]
  -r, --rubric-id TEXT      The Rubric ID of the target.
  -i, --input-file PATH     CSV/XLS(X) file with grades.  [required]
  --sheet INTEGER           The sheet id in XLS(X) file  [default: 0]
  --no-sum                  Use the last row of the grade file as the total
                            grade.

  --header                  Use the first row of the grade file as
                            description.

  --no-comment              Do not add a update comment in the submission
                            comments.

  --debug                   Debug mode.
  --dry-run                 Nothing is actually updated, the actions to be
                            performed are written to the terminal.

  -h, --help                Show this message and exit.
  --version                 Show the version and exit.

```

## Sample Usage

```bash
canvasautorubric -u https://umjicanvas.com/ -k Yy8WeJFndZ2oeorbQ3K0TMJ98u4l5QvftTe1YQgaemFVfxvNsLexSSja7SYx6hgX -c 786 -a 7081 -r 182 -i sample.csv
```

