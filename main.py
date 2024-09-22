import subprocess
import os
from os.path import dirname, abspath, join
import json
# from src.face_checkers.face_checker_factory import FaceCheckerFactory
# from src.utils import load_target_image, save_final_image

root = dirname(abspath(__file__))

try:
    blender_exe_path_keeper = join(
        root,
        "config",
        "path_blender_exe.json",
    )

    with open(blender_exe_path_keeper, "r") as file:
        data = json.load(file)

    blender_exe_path = data["path"]

except FileNotFoundError:
    blender_exe_path = "blender"

blend_file = join(root, "human-face_generator.blend")
python_script = join(root, "src", "hfgenerator.py")

THRESHOLD = 0.9

def run_blender_script():
    command = [blender_exe_path, blend_file, "--background", "--python", python_script]
    subprocess.run(command)


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

def test():
    run_blender_script()
    # Add any testing logic here

if __name__ == "__main__":
    # main()
    test()
