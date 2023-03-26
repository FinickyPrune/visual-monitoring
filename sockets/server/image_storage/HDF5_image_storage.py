import logging
import os
import numpy as np
import h5py
from PIL import Image

from server.image_storage.image_storage_interface import ImageStorageInterface
from pathlib import Path


class HDF5ImageStorage(ImageStorageInterface):

    hdf5_dir = Path("data/hdf5/")
    file_names: [str] = []

    def __init__(self):
        self.hdf5_dir.mkdir(parents=True, exist_ok=True)
        for file in os.listdir(self.hdf5_dir):
            self.file_names.append(file.title()[:-3])
        logging.info(self.file_names)

    def save(self, image, name):
        count = len(os.listdir(self.hdf5_dir))
        file_name = f"{count}_{name}.h5"
        file = h5py.File(self.hdf5_dir / file_name, "w")
        file.create_dataset(
            "image", np.shape(image), h5py.h5t.STD_U8BE, data=image
        )
        file.close()
        self.file_names.append(file_name[:-3])

    def load(self, image_name) -> Image:
        file = h5py.File(self.hdf5_dir / f"{image_name}.h5", "r+")
        image = np.array(file["/image"]).astype("uint8")
        return Image.fromarray(image)

    def files_names(self) -> [str]:
        return self.file_names

