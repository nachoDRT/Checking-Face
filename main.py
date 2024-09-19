from src.hfgenerator import HFGenerator
from src.face_checkers.face_checker_factory import FaceCheckerFactory
from src.utils import load_target_image, save_final_image


THRESHOLD = 0.9

def main():
    face_checker = FaceCheckerFactory.get_face_checker("visual_llm")
    face_checker.load()
    human_face_generator = HFGenerator()

    target_image = load_target_image()
    current_image = human_face_generator.generate_initial_face()

    while True:
        similarity_score, differences = face_checker.check_faces(target_image, current_image)
        
        if similarity_score > THRESHOLD:
            break
        
        instructions = face_checker.generate_instructions(differences)
        current_image = human_face_generator.modify_face(instructions)

    save_final_image(current_image)



if __name__ == "__main__":
    main()
