from datetime import datetime
import logging
from typing import List

from ischedule import schedule, run_loop
from datetime import timedelta

from models.image import ImageDto
from server.image_storage.image_storage_interface import ImageStorageInterface
from server.observer_interface.observer import Subject, Observer
from server.sync_manager.sync_manager import SyncManager
from utils.constants import (
    UPDATE_STORAGE_INTERVAL,
    LOOP_DURATION,
    TIMESTAMP_FORMAT,
    DELIMITER, BUFFER_CHUNK,
)


class ImageBuffer(Subject):
    image_storage: ImageStorageInterface
    image_dtos: list[ImageDto] = []

    observers: List[Observer] = []

    def __init__(self, image_storage, observer):
        self.image_storage = image_storage
        self.observers.append(observer)
        images, file_names = self.image_storage.load_all()
        for i in range(len(images)):
            timestamp: datetime = datetime.strptime(
                file_names[i].split(DELIMITER)[2], TIMESTAMP_FORMAT
            )
            self.image_dtos.append(ImageDto(timestamp, images[i]))
        SyncManager.sort_images(self.image_dtos)
        if len(self.image_dtos) >= BUFFER_CHUNK:
            self.notify()
        schedule(self.update_buffer, interval=UPDATE_STORAGE_INTERVAL)
        run_loop(return_after=timedelta(hours=LOOP_DURATION))

    def update_buffer(self):
        images = []
        file_names = []
        if len(self.image_dtos) == 0:
            images, file_names = self.image_storage.load_all()
        else:
            timestamp = self.image_dtos[-1].timestamp
            images, file_names = self.image_storage.load_all_after(timestamp)

        for i in range(len(images)):
            timestamp: datetime = datetime.strptime(
                file_names[i].split(DELIMITER)[2], TIMESTAMP_FORMAT
            )
            self.image_dtos.append(ImageDto(timestamp, images[i]))
        SyncManager.sort_images(self.image_dtos)
        if len(self.image_dtos) >= BUFFER_CHUNK:
            self.notify()
        logging.info(images)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)
