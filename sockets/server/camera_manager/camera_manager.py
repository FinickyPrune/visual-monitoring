import uuid
import logging
from models.image import ImageRawData


class CameraManager:
    camera_dict = dict()

    def register_camera(self, addr):
        self.camera_dict[addr] = [uuid.uuid4().hex[:6].upper(), ImageRawData()]
        logging.info("Registered camera with uuid " + self.camera_dict[addr][0])

    def unregister_camera(self, addr):
        logging.info("Unregistered camera with uuid " + self.camera_dict[addr][0])
        self.camera_dict.pop(addr)

    def image_for_addr(self, addr):
        return self.camera_dict[addr][1]

    def uuid_for_addr(self, addr):
        return self.camera_dict[addr][0]

    def update_image(self, addr, image):
        self.camera_dict[addr][1] = image