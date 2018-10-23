import numpy as np
import matplotlib.pyplot as plt


def _build_three_groups_bars(group1, group2, group3, *, colors: tuple):
    n_groups = 3
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.3
    opacity = 0.8

    group1_color, group2_color, group3_color = colors

    bars_group1 = plt.bar(
        index, group1, bar_width,
        alpha=opacity,
        color=group1_color,
        label='raw',
    )

    bars_group2 = plt.bar(
        index + bar_width, group2, bar_width,
        alpha=opacity,
        color=group2_color,
        label='punctuation removed',
        )

    bars_group3 = plt.bar(
        index + 2*bar_width, group3, bar_width,
        alpha=opacity,
        color=group3_color,
        label='stopwords removed'
    )

    plt.xlabel('Sentiments')
    plt.ylabel('Tokens')
    plt.title('Tokens by sentiment')
    plt.xticks(index + bar_width, ('good', 'neutral', 'bad'))
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    colors = ('#2E4057', '#05668D', '#028090')
    words_raw = (569083, 28729, 17766)
    # Lowercase and punctuation removed
    words_punct_removed = (463130, 23225, 14400)
    # Stopwords removed
    words_stop_removed = (303990, 15128, 9330)
    # _build_three_groups_bars(
    #     words_raw,
    #     words_punct_removed,
    #     words_stop_removed,
    #     colors=colors,
    # )

    # recurrent
    colors_rec = ('#6DA34D', '#17B890', '#8FBC94')
    words_raw_rec = (61196, 8860, 6052)
    words_punct_removed_rec = (56599, 8379, 5727)
    words_stop_removed_rec = (56448, 8229, 5579)
    _build_three_groups_bars(
        words_raw_rec,
        words_punct_removed_rec,
        words_stop_removed_rec,
        colors=colors_rec,
    )


if __name__ == '__main__':
    main()
