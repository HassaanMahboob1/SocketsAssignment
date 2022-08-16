from pickle import DICT
import socket
import json
from _thread import *

host = socket.gethostname()
port = 5555
BUFFER = 1000
ThreadCount = 0
MessageList = []
dict_data = {"DateTime": "", "Message": "", "AuthorName": ""}


class Message:
    def __init__(self, uuid, datetime, message, authorname):
        self.Uuid = uuid
        self.DateTime = datetime
        self.Message = message
        self.AuthorName = authorname


def multi_threaded_client(conn):
    while True:
        data = conn.recv(BUFFER).decode()
        print(data)
        if not data:
            break
        data = json.loads(data)
        Uuid = data["Uuid"]
        DateTime = data["DateTime"]
        message = str(data["Message"])
        AuthorName = data["AuthorName"]
        Obj = Message(Uuid, DateTime, message, AuthorName)
        if message.lower().strip() == "sync":
            for i in range(len(MessageList)):
                uuid = "Uuid" + str(i)
                dt = "DateTime" + str(i)
                msg = "Message" + str(i)
                an = "AuthorName" + str(i)
                dict_data[uuid] = MessageList[i].Uuid
                dict_data[dt] = MessageList[i].DateTime
                dict_data[msg] = MessageList[i].Message
                dict_data[an] = MessageList[i].AuthorName
            json_data = json.dumps(dict_data)
            conn.send(bytes(json_data, encoding="utf-8"))
        MessageList.append(Obj)

    for i in range(len(MessageList)):
        print(MessageList[i].Uuid)
        print(MessageList[i].DateTime)
        print(MessageList[i].Message)
        print(MessageList[i].AuthorName)

    conn.close()


server_socket = socket.socket()
port = input("Enter your port")
server_socket.bind((host, int(port)))
print("Server started successfully\nWaiting for client to connect")
server_socket.listen(5)
while True:
    Client, address = server_socket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    start_new_thread(multi_threaded_client, (Client,))
    ThreadCount += 1
    print("Thread Number: " + str(ThreadCount))

server_socket.close()
