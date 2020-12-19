# Usage

```bash
Usage: canvasautoplot [OPTIONS]

Options:
  -i, --input-file PATH   CSV/XLSX input file with grades.  [required]
  -o, --output-file PATH  PNG/EPS/PDF output file with distribution.
                          [required]

  --column INTEGER        Plot the specific column (the last column is -1).
                          [default: -1]

  --sum                   Plot the sum of all columns, will ignore the
                          --column parameter.

  --header                Skip the first row.
  --preview               Preview the plot before output.
  --xmin INTEGER          Min value of x-axis (grade).  [default: 0]
  --xmax INTEGER          Max value of x-axis (grade).  [default: 100]
  --bins INTEGER          Number of histogram bins.  [default: 20]
  --ytick INTEGER         Step between labels of y-axis (frequency).
                          [default: 5]

  --title TEXT            Title of the plot.  [default: Grades Plot]
  -h, --help              Show this message and exit.
  --version               Show the version and exit.

```

## Sample Usage

```bash
canvasautoplot -i sample.csv -o sample.pdf --ytick 2 --preview
```

