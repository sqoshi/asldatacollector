import os
import pickle
import random
from pathlib import Path

import cv2
from mediapipe.python.solutions.hands import Hands


def process_image(hands: Hands, img_path: str):
    """Process a single image and extract hand landmarks."""
    data_aux = []
    x_, y_ = [], []
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                x_.append(landmark.x)
                y_.append(landmark.y)

            # Normalize landmarks to the top-left corner
            for landmark in hand_landmarks.landmark:
                data_aux.append(landmark.x - min(x_))
                data_aux.append(landmark.y - min(y_))
        return data_aux, True

    return None, False


def process_all(
    dir: str,
    output: str = "data.pickle",
    batch: int = 100,
):
    """Process all classes across all sample directories in batches."""
    hands = Hands(
        max_num_hands=1,
        static_image_mode=True,
        min_detection_confidence=0.3,
    )
    result = {"data": [], "labels": []}
    all_images = [str(file) for file in Path(dir).rglob("*") if file.is_file()]
    random.shuffle(all_images)
    for img_path in all_images:
        data_aux, valid = process_image(hands, img_path)
        if valid:
            label = img_path.split(os.path.sep)[-2]
            result["data"].append(data_aux)
            result["labels"].append(label)

    # # Display stats after processing
    # unique_labels, counts = np.unique(all_labels, return_counts=True)
    # print_class_stats(unique_labels, counts)
    # draw_class_bar_plot(unique_labels, counts)
    with open(output, "wb") as f:
        pickle.dump(result, f)
