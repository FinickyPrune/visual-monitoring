import logging
from abc import ABC
from typing import List
from itertools import combinations
import numpy as np
from sympy.geometry import Line2D, Point2D
from numpy.linalg import norm

from server.objects_recognizer.objects_recognizer import ObjectRecognizer
from server.objects_recognizer.recognizable_object.recognizable_object_interface import (
    RecognizableObjectInterface,
)
from server.observer_interface.observer import Observer, Subject


class Estimator(Observer, Subject, ABC):
    observers: List[Observer] = []

    ideal_path: List[List[float]] = []
    real_path: List[List[float]] = []

    def __init__(self, observer):
        self.observers.append(observer)

    def estimate(self, objects: list[RecognizableObjectInterface]):
        logging.debug("Estimating...")
        self.ideal_path = []
        self.real_path = []

        self.real_path.extend([obj.coordinates for obj in objects])
        self.ideal_path.extend([[0.00, 0.00]] * 5)

        for index in range(len(objects) - 5):
            r = [obj.coordinates for obj in objects[index: index + 5]]
            c = np.array(list(combinations(r, 2)))
            guide_vector_points = np.mean(c[:, 0, :], axis=0), np.mean(c[:, 1, :], axis=0)

            line = Line2D(Point2D(guide_vector_points[0]), Point2D(guide_vector_points[1]))

            r_last = r[-1]
            r_projected = line.projection(r_last)

            facing = np.array([obj.towards for obj in objects[index: index + 5]])

            t = [obj.timestamp.microsecond for obj in objects[index: index + 5]]

            mean_facing = np.mean(facing, axis=0)

            dr = norm(np.diff(r, axis=0), axis=1)
            dt = np.diff(t, axis=0)

            v_mean = np.sum(dr) / np.sum(dt)

            r_predicted = r_projected + v_mean * np.mean(dt, axis=0) * mean_facing

            self.ideal_path.append(list(r_predicted))
        self.notify()

    def update(self, subject: ObjectRecognizer) -> None:
        self.estimate(objects=subject.objects)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)
