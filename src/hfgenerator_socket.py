import bpy
import socket

# Socket server configuration in Blender
host = ''  # Listen on all interfaces
port = 12347  # Arbitrary port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Server listening on port {port}")

def apply_lighting_changes(data):
    """
    Function that applies lighting changes based on received data.
    """
    light_data = data.split(' ')
    light = bpy.data.objects.get('Light')
    
    if light:
        light.location.x = float(light_data[0])
        light.location.y = float(light_data[1])
        light.location.z = float(light_data[2])
        light.data.energy = float(light_data[3])  # Change light intensity
        print(f"Lighting updated: {light.location}, Energy: {light.data.energy}")
    else:
        print("No light object named 'Light' found.")

def render_scene():
    """
    Function that executes the rendering.
    """
    print("Rendering scene...")
    bpy.ops.render.render(write_still=True)
    print("Render complete.")

while True:
    print("Waiting for a new connection...")
    conn, addr = server_socket.accept()
    print(f'Connection from {addr}')

    while True:
        try:
            # Receive data from the client
            data = conn.recv(1024)
            if not data:
                print("No data, but keeping connection open.")
                break  # Doesn't close the connection

            # Process received data
            received_info = data.decode('utf-8')
            print(f"Client says: {received_info}")

            # Interpret client commands
            if received_info.startswith("light"):  # Lighting changes
                light_data = received_info.split(" ", 1)[1]
                apply_lighting_changes(light_data)
            elif received_info == "render":  # Render command
                render_scene()
            elif received_info == "exit":  # Close connection
                print("Closing connection as per client request.")
                conn.close()
                break  # Exits the inner loop and waits for a new connection

            # Send a response to the client
            conn.sendall(b'ack')

        except socket.error:
            print("Socket error, closing connection.")
            conn.close()
            break
