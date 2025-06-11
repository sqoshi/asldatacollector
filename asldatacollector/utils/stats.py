from collections import defaultdict
import logging
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt


# def draw_class_bar_plot(
#     labels: List[str], counts: List[int], threshold_scale: float = 0.5
# ) -> None:
#     max_count = np.max(counts)
#     threshold = threshold_scale * max_count
#     plt.figure(figsize=(12, 6))
#     bars = plt.bar(labels, counts, color="b")
#     for bar, count in zip(bars, counts):
#         if count < threshold:
#             bar.set_color("r")
#     plt.xlabel("Class Labels")
#     plt.ylabel("Number of Elements")
#     plt.title("Class Distribution")
#     plt.axhline(
#         y=threshold, color="gray", linestyle="--", label=f"Threshold: {threshold}"
#     )
#     plt.legend()

#     for bar, count in zip(bars, counts):
#         plt.text(
#             bar.get_x() + bar.get_width() / 2,
#             bar.get_height(),
#             str(count),
#             ha="center",
#             va="bottom",
#         )
#     plt.show()
#     plt.savefig("class_distribution.png")


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

def draw_class_bar_plot(
    labels: List[str], counts: List[int], threshold_scale: float = 0.5
) -> None:
    max_count = np.max(counts)
    threshold = 800  # threshold_scale * max_count
    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, counts, color="b")

    # Change bar colors based on the threshold
    for bar, count in zip(bars, counts):
        if count < threshold:
            bar.set_color("b")

    plt.xlabel("Class Labels")
    plt.ylabel("Number of Elements")
    plt.title("ASL-hands Class Distribution")
    plt.axhline(
        y=threshold, color="gray", linestyle="--", label=f"Threshold: {threshold}"
    )
    plt.ylim(0, 2000)
    plt.legend()

    # Add labels on top of each bar with a 90 degree rotation
    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height()+25,
            str(count),
            ha="center",
            va="bottom",
            rotation=90,  # Rotate the text labels by 90 degrees
            fontsize=12  # Set the font size
        )
        bar.set_label(f"{count}")
    
    plt.xticks(
        ticks=range(0, len(labels), 1),  # Step size of 2 for tick positions
        labels=labels  # Only show every second label
    )
    # Save the figure before showing it
    plt.savefig("aslhands_class_distro_preprocessed.png")
    plt.show()

def scan_mnist():
    import pandas as pd

    df = pd.read_csv(
        "/home/piotr/Workspaces/studies/htt-models/data/mnist/sign_mnist_train/sign_mnist_train.csv"
    )
    column_data = df.iloc[1:, 0].to_numpy()
    array_data = column_data
    unique_elements = set(array_data)
    element_counts = {
        element: list(array_data).count(element) for element in unique_elements
    }
    element_counts[9] = 0
    element_counts[25] = 0
    return element_counts


def scan_filesystem(base_dir: str):
    label_counts = defaultdict(int)

    for person_dir in os.listdir(base_dir):
        person_path = os.path.join(base_dir, person_dir)

        if os.path.isdir(person_path):
            for label_dir in os.listdir(person_path):
                label_path = os.path.join(person_path, label_dir)

                if os.path.isdir(label_path):
                    image_count = len(os.listdir(label_path))
                    label_counts[label_dir] += image_count

    return label_counts


if __name__ == "__main__":
    res = scan_filesystem("/home/piotr/Documents/htt/images")
    # res = scan_mnist()
    res = dict(sorted(res.items(), key=lambda x: int(x[0])))
    labels = list(res.keys())
    counts = list(res.values())
    draw_class_bar_plot(labels, counts)
