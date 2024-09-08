# -*- coding: utf-8 -*-
import logging
import os
import pickle

import cv2
import numpy as np
from mediapipe.python.solutions.hands import Hands

from ..utils.statistics import draw_class_bar_plot, print_class_stats

DATA_DIR = "./data"


def process():
    hands = Hands(max_num_hands=1, static_image_mode=True, min_detection_confidence=0.3)

    data = []
    labels = []

    for dir_ in sorted(os.listdir(DATA_DIR), key=lambda x: int(x)):
        for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
            data_aux = []
            x_, y_ = [], []
            img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x_.append(hand_landmarks.landmark[i].x)
                        y_.append(hand_landmarks.landmark[i].y)

                    for i in range(len(hand_landmarks.landmark)):
                        data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                        data_aux.append(hand_landmarks.landmark[i].y - min(y_))
                data.append(data_aux)
                labels.append(dir_)
            else:
                logging.info(
                    "warning hand landmakrs unrecognized in image {}/{}".format(
                        dir_, img_path
                    )
                )
    unique_labels, counts = np.unique(labels, return_counts=True)
    print_class_stats(unique_labels, counts)
    draw_class_bar_plot(unique_labels, counts)

    with open("data.pickle", "wb") as f:
        pickle.dump({"data": data, "labels": labels}, f)
