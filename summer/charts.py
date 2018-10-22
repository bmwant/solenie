import numpy as np
import matplotlib.pyplot as plt


def main():
    # data to plot
    n_groups = 3
    words_raw = (90, 55, 40)
    words_punkt_removed = (85, 62, 54)
    words_stop_removed = (73, 50, 43)

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.3
    opacity = 0.8

    bars_raw = plt.bar(
        index, words_raw, bar_width,
        alpha=opacity,
        color='#2E4057',
        label='raw',
    )

    bars_punct_removed = plt.bar(
        index + bar_width, words_punkt_removed, bar_width,
        alpha=opacity,
        color='#05668D',
        label='punctuation removed',
    )

    bars_stop_removed = plt.bar(
        index + 2*bar_width, words_stop_removed, bar_width,
        alpha=opacity,
        color='#028090',
        label='stopwords removed'
    )
    #2D93AD
    plt.xlabel('Sentiments')
    plt.ylabel('Tokens')
    plt.title('Tokens by sentiment')
    plt.xticks(index + bar_width, ('good', 'neutral', 'bad'))
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
