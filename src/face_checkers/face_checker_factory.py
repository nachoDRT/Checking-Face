from .visual_llm_face_checker import VisualLLMFaceChecker

class FaceCheckerFactory:
    @staticmethod
    def get_face_checker(checker_name):
        if checker_name == "visual_llm":
            return VisualLLMFaceChecker()
        else:
            raise ValueError(f"Face checker {checker_name} not supported")