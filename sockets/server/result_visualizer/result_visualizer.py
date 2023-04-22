import logging
from abc import ABC

from server.estimator.estimator import Estimator
from server.observer_interface.observer import Observer


class ResultVisualizer(Observer, ABC):

    def display(self, ideal_path: [[float]], real_path: [[float]]):
        logging.debug("I      R      ")
        for index in range(len(ideal_path)):
            logging.debug(f"{ideal_path[index]}     {real_path[index]}")

    def update(self, subject: Estimator) -> None:
        self.display(subject.ideal_path, subject.real_path)
