import logging
from typing import List

import numpy as np
from matplotlib import pyplot as plt


def draw_class_bar_plot(
    labels: List[str], counts: List[int], threshold_scale: float = 0.5
) -> None:
    max_count = np.max(counts)
    threshold = threshold_scale * max_count
    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, counts, color="b")
    for bar, count in zip(bars, counts):
        if count < threshold:
            bar.set_color("r")
    plt.xlabel("Class Labels")
    plt.ylabel("Number of Elements")
    plt.title("Class Distribution")
    plt.axhline(
        y=threshold, color="gray", linestyle="--", label=f"Threshold: {threshold}"
    )
    plt.legend()

    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(count),
            ha="center",
            va="bottom",
        )
    plt.show()
    plt.savefig("class_distribution.png")


def print_class_stats(
    labels: List[str],
    counts: List[int],
):
    logging.info(
        f"missing classes for {set(labels).difference([str(i) for i in range(26)])}"
    )
    for label, count in zip(labels, counts):
        msg = f"Class {label}: {count} elements"
        if count < 35:
            msg += " - should be retaken"
        logging.info(msg)
