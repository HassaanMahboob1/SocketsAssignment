from sqlite3 import Date
import uuid
import datetime
import socket
import json
import threading

host = socket.gethostname()
ip = socket.gethostbyname(host)
print(ip)
nport = 5555
BUFFER = 1000


def multi_threaded_client(port):
    print("socket is listening")
    peersocket = socket.socket()
    peersocket.bind((host, port))
    peersocket.listen(5)
    peersocket.accept()
    print("connect with  new port")


Uuid = uuid.uuid4()
DateTime = datetime.datetime.now()
client_socket = socket.socket()
port = int(input("Enter your port"))

connectionThread = threading.Thread(target=multi_threaded_client, args=(port,))
try:
    while True:
        port_connect = input("Enter port you want to connect")
        client_socket.connect((host, int(port_connect)))
        dict_data = {"DateTime": "", "Message": "", "AuthorName": ""}
        Message_input = input("Enter Message : ")
        Author_name_input = input("Enter Author name : ")

        dict_data["DateTime"] = str(DateTime)
        dict_data["Message"] = Message_input
        dict_data["AuthorName"] = Author_name_input

        new_dict = dict()

        while Message_input.lower().strip() != "end":
            Uuid = uuid.uuid4()
            new_dict[str(Uuid.hex)] = dict_data
            json_data = json.dumps(new_dict)
            client_socket.send(bytes(json_data, encoding="utf-8"))
            if Message_input.lower().strip() == "sync":
                print("Waiting for response from server ! ")
                data = client_socket.recv(BUFFER).decode()
                data = json.loads(data)
                print(data)
            Message_input = input("Enter Message : ")
            Author_name_input = input("Enter Author name : ")
            dict_data["Uuid"] = str(Uuid)
            dict_data["DateTime"] = str(DateTime)
            dict_data["Message"] = Message_input
            dict_data["AuthorName"] = Author_name_input

except:
    client_socket.close()
    connectionThread.start()
    other_socket = socket.socket()
    other_port = int(input("Enter the other port"))
    other_socket.connect(
        (host, other_port),
    )
