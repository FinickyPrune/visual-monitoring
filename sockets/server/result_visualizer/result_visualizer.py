import logging
from abc import ABC

from server.estimator.estimator import Estimator
from server.observer_interface.observer import Observer


class ResultVisualizer(Observer, ABC):

    def display(self, ideal_path: [[float]], real_path: [[float]]):
        logging.debug("R      I      ")
        for index in range(len(ideal_path)):
            logging.debug(f"[{real_path[index][0]:.2f} {real_path[index][1]:.2f}] [{ideal_path[index][0]:.2f} {ideal_path[index][1]:.2f}]")

    def update(self, subject: Estimator) -> None:
        self.display(subject.ideal_path, subject.real_path)
