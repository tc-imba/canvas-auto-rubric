from canvasautorubric import utils
import click

from scipy.stats import gaussian_kde, norm
import numpy as npy
import matplotlib.pyplot as plt


def plot_distribution(scores, title='Grades', xmin=0, xmax=100, bins=20, ytick=5, filename='fig.pdf', preview=False):
    x_grid = npy.linspace(xmin, xmax, 2000)
    bin_grid = npy.linspace(xmin, xmax, bins + 1)
    mean = npy.around(npy.mean(scores), 3)
    std = npy.around(npy.std(scores), 3)
    q1 = npy.around(npy.quantile(scores, 0.25), 3)
    q2 = npy.around(npy.quantile(scores, 0.5), 3)
    q3 = npy.around(npy.quantile(scores, 0.75), 3)

    # bandwidth = 0.2
    kde = gaussian_kde(scores)
    trans = len(scores) * (xmax - xmin) / bins
    pdf_estimate = kde.evaluate(x_grid) * trans
    pdf_normal = norm(mean, std).pdf(x_grid) * trans
    # print(pdf_normal)

    count, _ = npy.histogram(scores, bins=bin_grid)
    ymax = npy.ceil(npy.max(count) / ytick) * ytick

    fig = plt.figure(figsize=(10, 10), dpi=100)
    plt.rcParams.update({'font.size': 16, 'font.family': 'monospace'})

    plt.hist(scores, fill=False, bins=bin_grid)
    plt.plot(x_grid, pdf_normal, color='blue', linewidth=1, label='Normal Distribution')
    plt.plot(x_grid, pdf_estimate, color='red', linewidth=1, dashes=[2, 2], label='Estimated Distribution')

    # locs, labels = plt.yticks()
    box_width = ymax / 5
    plt.boxplot(scores, vert=False, widths=box_width, positions=[ymax + box_width * 2])
    locs = npy.arange(0, ymax + 1, ytick)
    labels = map(lambda x: str(int(x)), locs)
    plt.yticks(locs, labels)
    plt.ylim(0, ymax + box_width * 5)

    with npy.printoptions(precision=3):
        text = '  Q1: %s\n  Q2: %s\n  Q3: %s\nMean: %s\n Std: %s\n' % (q1, q2, q3, mean, std)
    plt.text(0, ymax + box_width * 4.5, text, verticalalignment='top')

    plt.legend()
    plt.title(title)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    if preview:
        plt.show()
    fig.savefig(fname=filename)


@click.command()
@click.option('-i', '--input-file', required=True, type=click.Path(exists=True),
              help='CSV/XLSX input file with grades.')
@click.option('-o', '--output-file', required=True, type=click.Path(),
              help='PNG/EPS/PDF output file with distribution.')
@click.option('--column', default=-1, show_default=True, help='Plot the specific column (the last column is -1).')
@click.option('--sum', is_flag=True, help='Plot the sum of all columns, will ignore the --column parameter.')
@click.option('--header', is_flag=True, help='Skip the first row.')
@click.option('--preview', is_flag=True, help='Preview the plot before output.')
@click.option('--xmin', default=0, show_default=True, help='Min value of x-axis (grade).')
@click.option('--xmax', default=100, show_default=True, help='Max value of x-axis (grade).')
@click.option('--bins', default=20, show_default=True, help='Number of histogram bins.')
@click.option('--ytick', default=5, show_default=True, help='Step between labels of y-axis (frequency).')
@click.option('--title', default='Grades Plot', show_default=True, help='Title of the plot.')
@click.help_option('-h', '--help')
@click.version_option(version=utils.get_version())
def main(input_file, output_file, column, sum, header, preview, xmin, xmax, bins, ytick, title):
    df = utils.read_data(input_file, header)
    if sum:
        data = df.sum(1)
    else:
        data = df.iloc[:, column]
    plot_distribution(data, xmin=xmin, xmax=xmax, bins=bins, title=title, ytick=ytick, filename=output_file,
                      preview=preview)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
    # df = utils.read_data('Final_Grades.xlsx', True)
    # plot_distribution(df.iloc[:, -1], xmax=40, title='VV186 Final', filename='final.pdf')
    # df = utils.read_data('Mid2_Grades.xlsx', True)
    # plot_distribution(df.iloc[:, -1], xmax=30, title='VV186 Midterm 2', filename='mid2.pdf')
