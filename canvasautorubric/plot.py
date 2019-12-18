from canvasautorubric import utils

from scipy.stats import gaussian_kde, norm
import numpy as npy
import matplotlib.pyplot as plt


def plot_distribution(scores, title='Grades', xmin=0, xmax=100, bins=20, ytick=5, filename='fig.pdf'):
    x_grid = npy.linspace(xmin, xmax, 2000)
    bin_grid = npy.linspace(xmin, xmax, bins + 1)
    mean = npy.mean(scores)
    std = npy.std(scores)
    q1 = npy.quantile(scores, 0.25)
    q2 = npy.quantile(scores, 0.5)
    q3 = npy.quantile(scores, 0.75)

    # bandwidth = 0.2
    kde = gaussian_kde(scores)
    trans = len(scores) * (xmax - xmin) / bins
    pdf_estimate = kde.evaluate(x_grid) * trans
    pdf_normal = norm(mean, std).pdf(x_grid) * trans
    # print(pdf_normal)

    count, _ = npy.histogram(scores, bins=bin_grid)
    ymax = npy.ceil(npy.max(count) // ytick) * ytick

    fig = plt.figure(figsize=(10, 10), dpi=100)
    plt.rcParams.update({'font.size': 16, 'font.family': 'monospace'})

    plt.hist(scores, fill=False, bins=bin_grid)
    plt.plot(x_grid, pdf_normal, color='blue', linewidth=1, label='Normal Distribution')
    plt.plot(x_grid, pdf_estimate, color='red', linewidth=1, dashes=[2, 2], label='Estimated Distribution')

    locs, labels = plt.yticks()
    box_width = ymax / 5
    plt.boxplot(scores, vert=False, widths=box_width, positions=[ymax + box_width * 2])
    labels = map(lambda x: str(int(x)), locs)
    plt.yticks(locs, labels)
    plt.ylim(0, ymax + box_width * 5)

    with npy.printoptions(precision=3):
        mean = npy.round(mean, decimals=3)
        std = npy.round(std, decimals=3)
        text = '  Q1: %s\n  Q2: %s\n  Q3: %s\nMean: %s\n Std: %s\n' % (q1, q2, q3, mean, std)
    plt.text(0, ymax + box_width * 4.5, text, verticalalignment='top')

    plt.legend()
    plt.title(title)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()
    fig.savefig(fname=filename)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    df = utils.read_data('Final_Grades.xlsx', True)
    plot_distribution(df.iloc[:, -1], xmax=40, title='VV186 Final', filename='final.pdf')
    df = utils.read_data('Mid2_Grades.xlsx', True)
    plot_distribution(df.iloc[:, -1], xmax=30, title='VV186 Midterm 2', filename='mid2.pdf')
