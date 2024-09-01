import logging
import os

import cv2
from mediapipe.python.solutions.hands import Hands

from .utils import get_letter, get_relative_path


def create_directory(path: str):
    """Create a directory if it doesn't exist."""
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


def capture_image(cap, hands, output_dir: str):
    """Capture and save a single image if hand landmarks are detected."""
    ret, frame = cap.read()
    if not ret:
        return False

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        file_name = f"{len(os.listdir(output_dir)) + 1}.jpg"
        cv2.imwrite(os.path.join(output_dir, file_name), frame)
        return True
    return False


def show_image_from_file(image_path: str = ""):
    """Display an image from a file in a separate window."""
    if not image_path:
        image_path = get_relative_path("assets", "alphabet.png")
    if not os.path.exists(image_path):
        logging.warning(f"Image file {image_path} not found")
        return
    image = cv2.imread(image_path)
    if image is not None:
        cv2.imshow("Image from File", image)
        cv2.waitKey(1)
    else:
        logging.info(f"Failed to load image from {image_path}")


def collect_class_data(
    class_id: int, dataset_size: int, cap, hands: Hands, data_dir: str
):
    """Collect data for a specific class."""
    output_dir = os.path.join(data_dir, str(class_id))
    create_directory(output_dir)

    while len(os.listdir(output_dir)) < dataset_size:
        if capture_image(cap, hands, output_dir):
            cv2.imshow("frame", cap.read()[1])
            cv2.waitKey(25)


def collect_data(
    data_dir: str,
    number_of_classes: int = 26,
    dataset_size: int = 100,
    capture_device: int = 0,
):
    """Main function to collect data for all classes."""
    create_directory(data_dir)
    hands = Hands(static_image_mode=True, min_detection_confidence=0.3)
    cap = initialize_capture_device(capture_device)
    show_image_from_file()

    for class_id in range(number_of_classes):
        logging.info(f"Collecting data for class {class_id}")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            display_instructions(frame, class_id)
            cv2.imshow("frame", frame)
            if cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
                cap.release()
                cv2.destroyAllWindows()
                return
            if cv2.waitKey(25) == ord("q"):
                break

        collect_class_data(class_id, dataset_size, cap, hands, data_dir)
        if cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
