import logging

from server.objects_recognizer.recognizable_object.recognizable_object_interface import RecognizableObjectInterface


class Estimator:

    def estimate(self, objects: [RecognizableObjectInterface]):
        logging.debug("Estimating...")
