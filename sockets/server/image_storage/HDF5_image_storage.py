import numpy as np

from server.image_storage.image_storage_interface import ImageStorageInterface
from pathlib import Path
import h5py


class HDF5ImageStorage(ImageStorageInterface):

    hdf5_dir = Path("data/hdf5/")

    def __init__(self):
        self.hdf5_dir.mkdir(parents=True, exist_ok=True)

    def save(self, image, name):
        file = h5py.File(self.hdf5_dir / f"{name}.h5", "w")
        file.create_dataset(
            "image", np.shape(image), h5py.h5t.STD_U8BE, data=image
        )
        file.close()
