import socket
import os
import struct

HOST='192.168.1.25'
PORT=8000
file_pathSave="filePath"
Save_Folder=r'file_pathSave'
File_send=r'save_Folder'


def send_file():
    file_name=os.path.basename(File_send).encode("utf-8")
    file_size=os.path.getsize(File_send)

    print(f"sending file: {file_name.decode()}")
    print(f"File size :{file_size} bytes")
    print(f"sending to {HOST}:{PORT}")

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
        client_socket.connect(HOST,PORT)
        client_socket.sendall(struct.pack("!I",len(file_name)))
        client_socket.sendall(struct.pack("!I",file_size))
        client_socket.sendall(file_name)

        with open(File_send,"rb") as file:
            while chunk:=file.read(4096):
                client_socket.sendall(chunk)
        
    print("File send successfully")

if __name__=="__main__":
    send_file()
