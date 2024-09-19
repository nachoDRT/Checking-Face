from abc import ABC, abstractmethod

class BaseFaceChecker(ABC):
    @abstractmethod
    def check_faces(self, target_image, current_image):
        pass

    @abstractmethod
    def generate_instructions(self, differences):
        pass

    @abstractmethod
    def load(self):
        pass