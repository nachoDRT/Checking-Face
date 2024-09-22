import subprocess
import os
from os.path import dirname, abspath, join
import json
import socket
import time
from subprocess import Popen
# from src.face_checkers.face_checker_factory import FaceCheckerFactory
# from src.utils import load_target_image, save_final_image


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


def send_command_to_blender(command):
    host = "localhost"
    port = 12345  # Port used by the server in Blender

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send the command
    client_socket.send(command.encode('utf-8'))

    # Receive the response from Blender
    response = client_socket.recv(1024).decode('utf-8')
    print("Response from Blender:", response)

    client_socket.close()


def get_blender_path():
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
    python_script = join(root, "src", "hfgenerator_socket.py")
    
    return blender_exe_path, blend_file, python_script


def run_blender_script_popen(blender_exe_path, blend_file, python_script):
    blender_process = Popen([blender_exe_path, '-b', blend_file, '--python', python_script],  shell=True)

    # Wait for Blender to start the server
    time.sleep(10)

    # Example of sending lighting data
    lighting_command = "light 1.0 2.0 3.0 500.0"  # Change light position and energy
    send_command_to_blender(lighting_command)

    # Example of rendering
    render_command = "render"
    send_command_to_blender(render_command)
    
    lighting_command = "light 1.0 2.0 3.0 1500.0"  # Change light position and energy
    send_command_to_blender(lighting_command)
    time.sleep(10)

    # Example of rendering
    render_command = "render"
    send_command_to_blender(render_command)
    
    exit_command = "exit"
    send_command_to_blender(exit_command)

      
def send_command_to_blender(command):
    host = 'localhost'  # Or the IP if Blender is on another machine
    port = 12347  # The same port used by the server in Blender

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send the command
    client_socket.sendall(command.encode('utf-8'))

    # Receive the response from Blender
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received from Blender: {response}")

    client_socket.close()


def test():
    blender_exe_path, blend_file, python_script = get_blender_path()
    run_blender_script_popen(blender_exe_path, blend_file, python_script)


if __name__ == "__main__":
    # main()
    test()
