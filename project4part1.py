import socket
import os
import struct

HOST='ip'
PORT=8000
Save_Folder = r'C:\Users\You\Downloads'


def recv_exact(sock,size):
    data=b""
    while len(data)<size:
        part=sock.recv(size-len(data))
        if not part:
            raise ConnectionError("connection closed early")
        data+=part
    return data

def receive_file():

    os.makedirs(Save_Folder,exist_ok=True)
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        print("waiting for connection........")
        print(f"listening on {HOST}:{PORT}")
        print(f"Saving file to:{Save_Folder}")

        client_socket,client_adress=server_socket.accept()

        with client_socket:
            print("Connected to ",client_adress)

            name_length=struct.unpack("!I",recv_exact(client_socket,4))[0]
            file_size = struct.unpack("!Q", recv_exact(client_socket, 8))[0]
            file_name=recv_exact(client_socket,name_length).decode("utf-8")
            
            full_path=os.path.join(Save_Folder,file_name)

            received=0

            with open(full_path,"wb") as file:
                while received<file_size:
                    chunk =client_socket.recv(min(4096,file_size-received))
                    if not chunk:
                        break
                    file.write(chunk)       
                    received += len(chunk)
            print("file received successfully")


if __name__=="__main__":
    receive_file()


