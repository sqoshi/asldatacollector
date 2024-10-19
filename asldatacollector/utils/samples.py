import logging
import math
import os

import cv2
import numpy as np

from .helpers import get_letter


def calculate_grid_shape(total_classes: int) -> tuple:
    """Calculate the grid shape (rows, columns) based on the total number of classes."""
    cols = math.ceil(math.sqrt(total_classes))
    rows = math.ceil(total_classes / cols)
    return rows, cols


def load_and_resize_image(image_path: str, image_size: tuple) -> np.ndarray:
    """Load an image from a file and resize it."""
    sample_image = cv2.imread(image_path)
    if sample_image is None:
        logging.warning(f"Failed to load image from {image_path}")
        return None
    return cv2.resize(sample_image, image_size)


def place_image_in_grid(
    grid_image: np.ndarray,
    resized_sample: np.ndarray,
    class_label: str,
    image_size: tuple,
    row: int,
    col: int,
):
    """Place a resized image into the grid and add a label below it."""
    start_x = col * image_size[0]
    start_y = row * image_size[1]

    grid_image[start_y : start_y + image_size[1], start_x : start_x + image_size[0]] = (
        resized_sample
    )

    text_position = (start_x + 10, start_y + image_size[1] - 10)
    cv2.putText(
        grid_image,
        class_label,
        text_position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )


def create_class_samples_image(data_dir: str, image_size: tuple = (100, 100)):
    """
    Create an image that shows one sample from each class in a grid format with class labels.
    """
    class_dirs = sorted(
        [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    )
    total_classes = len(class_dirs)

    rows, cols = calculate_grid_shape(total_classes)
    logging.info(
        f"Automatically determined grid shape: {rows} rows, {cols} columns for {total_classes} classes."
    )

    grid_width = cols * image_size[0]
    grid_height = rows * image_size[1]
    grid_image = np.ones((grid_height, grid_width, 3), dtype=np.uint8) * 255

    for idx, class_dir in enumerate(class_dirs):
        class_label = get_letter(int(class_dir))
        class_path = os.path.join(data_dir, class_dir)
        sample_images = [f for f in os.listdir(class_path) if f.endswith(".jpg")]

        if not sample_images:
            logging.warning(f"No images found for class {class_label}")
            continue

        sample_image_path = os.path.join(class_path, sample_images[0])
        resized_sample = load_and_resize_image(sample_image_path, image_size)
        if resized_sample is None:
            continue

        row = idx // cols
        col = idx % cols
        place_image_in_grid(
            grid_image, resized_sample, class_label, image_size, row, col
        )

    return grid_image
