import logging
from abc import ABC
from typing import List

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
        for index in range(len(objects)):
            self.ideal_path.append(objects[index].coordinates)
            self.real_path.append(objects[index].coordinates)
        self.notify()

    def update(self, subject: ObjectRecognizer) -> None:
        self.estimate(objects=subject.objects)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)
