from abc import ABC, abstractmethod

from models.image import ImageDto


class Subject(ABC):

    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass

