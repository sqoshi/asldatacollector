import logging
import os

import cv2
from mediapipe.python.solutions.drawing_styles import (
    get_default_hand_connections_style,
    get_default_hand_landmarks_style,
)
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions.hands import HAND_CONNECTIONS, Hands

from asldatacollector.utils.helpers import get_letter
from asldatacollector.utils.samples import create_class_samples_image


def create_directory(path: str, drop: bool = False):
    """Create a directory if it doesn't exist."""
    if drop and os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
    if not os.path.exists(path):
        os.makedirs(path)


def initialize_capture_device(device_id: int):
    """Initialize and return the capture device."""
    return cv2.VideoCapture(device_id)


def display_instructions(frame, class_id: int):
    """Display instructions on the frame."""
    cv2.putText(
        frame,
        f"Press 'q' to collect data for class {class_id}: {get_letter(class_id)}",
        (100, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        3,
        cv2.LINE_AA,
    )


def show_image_from_file(image_path: str = ""):
    """Display an image from a file in a separate window."""
    if not image_path:
        image_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "alphabet.png"
        )
    if not os.path.exists(image_path):
        logging.warning(f"Image file {image_path} not found")
        return
    image = cv2.imread(image_path)
    if image is not None:
        cv2.imshow("Image from File", image)
        cv2.waitKey(1)
    else:
        logging.info(f"Failed to load image from {image_path}")


def collect_data(
    data_dir: str,
    number_of_classes: int = 26,
    dataset_size: int = 100,
    capture_device: int = 0,
    draw: bool = True,
    show_sample: bool = True,
):
    """Main function to collect data for all classes"""
    create_directory(data_dir)
    hands = Hands(static_image_mode=True, min_detection_confidence=0.3)
    cap = initialize_capture_device(capture_device)
    show_image_from_file()

    for class_id in range(number_of_classes):
        class_dir = os.path.join(data_dir, str(class_id))
        create_directory(class_dir, drop=True)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            display_instructions(frame, class_id)
            cv2.imshow("frame", frame)
            key = cv2.waitKey(25)
            if key == 27:
                cap.release()
                cv2.destroyAllWindows()
                return
            if key == ord("q"):
                break

        logging.info(f"Collecting data for class {class_id}")
        while len(os.listdir(class_dir)) < dataset_size:
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                file_name = f"{len(os.listdir(class_dir)) + 1}.jpg"
                cv2.imwrite(os.path.join(class_dir, file_name), frame)
                if draw:
                    for hl in results.multi_hand_landmarks:
                        draw_landmarks(
                            frame,
                            hl,
                            HAND_CONNECTIONS,
                            get_default_hand_landmarks_style(),
                            get_default_hand_connections_style(),
                        )
            else:
                logging.debug("Landmarks not visible")
            cv2.imshow("frame", frame)
            if cv2.waitKey(25) == 27:
                cap.release()
                cv2.destroyAllWindows()
                return
    if show_sample:
        samples_diag = create_class_samples_image(data_dir)
        cv2.imwrite("samples.png", samples_diag)
    cap.release()
    cv2.destroyAllWindows()
