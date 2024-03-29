from datetime import datetime
import logging
import os
from typing import List, Tuple
import numpy as np
import h5py
from PIL import Image

from server.image_storage.image_storage_interface import ImageStorageInterface
from pathlib import Path

from utils.constants import DELIMITER, TIMESTAMP_FORMAT


class HDF5ImageStorage(ImageStorageInterface):

    hdf5_dir = Path("data/hdf5/")
    file_names: List[str] = []

    def __init__(self):
        self.hdf5_dir.mkdir(parents=True, exist_ok=True)
        for file in os.listdir(self.hdf5_dir):
            self.file_names.append(file.title()[:-3])

    def save(self, image, name):
        count = len(os.listdir(self.hdf5_dir))
        file_name = f"{count}{DELIMITER}{name}.h5"
        file = h5py.File(self.hdf5_dir / file_name, "w")
        file.create_dataset("image", np.shape(image), h5py.h5t.STD_U8BE, data=image)
        file.close()
        self.file_names.append(file_name[:-3])

    def load(self, image_name) -> Image.Image:
        file = h5py.File(self.hdf5_dir / f"{image_name}.h5", "r+")
        image = np.array(file["/image"]).astype("uint8")
        return Image.fromarray(image)

    def load_all(self) -> Tuple[Image.Image, str]:
        images: List[Image.Image] = []
        file_names: List[str] = []
        for file in os.listdir(self.hdf5_dir):
            f = h5py.File(self.hdf5_dir / file, "r+")
            images.append(Image.fromarray(np.array(f["/image"]).astype("uint8")))
            file_names.append(file[:-3])
        return images, file_names

    def load_all_after(self, timestamp: datetime) -> Tuple[Image.Image, str]:
        images: List[Image.Image] = []
        file_names: List[str] = []
        for file in os.listdir(self.hdf5_dir):
            file_timestamp = datetime.strptime(
                Path(self.hdf5_dir / file).stem.split(DELIMITER)[2], TIMESTAMP_FORMAT
            )
            if timestamp >= file_timestamp:
                continue
            f = h5py.File(self.hdf5_dir / file, "r+")
            images.append(Image.fromarray(np.array(f["/image"]).astype("uint8")))
            file_names.append(file[:-3])
        return images, file_names

    def files_names(self) -> List[str]:
        return self.file_names
