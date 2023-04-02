#!/usr/bin/python3.9
import socket
import threading
from threading import Lock
import datetime
import os
from queue import Queue
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 7777))
sock.listen(5)
clientSocket, clientAddress = sock.accept()
print(clientAddress)

# Fac un Que ca sa pot sa sheruiesc date intre threaduri
threads_Data_Sharing_Q = Queue(maxsize=3)
quit_Queue = Queue(maxsize=2)
# Creez Variabila pentru lock
lock_thread = Lock()

# Creez un fisier LOG
today = datetime.datetime.today().strftime('%d%b%y')
# os.path.join(os.path.expanduser('~') - 
fisierLog = "/home/razvan/AdminRetele/Logs/" + "ChatLog" + str(today) + ".txt"

nowTime = datetime.datetime.now()
currentTime = (str(nowTime.hour), ':', str(nowTime.minute), ':', str(nowTime.second))
currentTime = ''.join(currentTime)
print(currentTime)

def append_new_line(fisierLog, textDeAdaugat):
    # Open the file in append & read mode ('a+')
    with open(fisierLog, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(textDeAdaugat)

#Mai jos folosesc ceva ce am descoperit cautand:
#ANSI escape codes:


WHITE = "\033[0m"
RED = "\033[38;2;255;25;25m"
BLUE = "\033[38;2;75;75;255m"
GREEN = "\033[38;2;60;255;60m"
CLEAR_DISPLAY = "\033[2J"
CLEAR_LINE = "\033[K"  # Clears characters from cursor position until the end of line
UP = "\033[1000A"  # Moves cursor 1000 positions up
UP_ONE = "\033[1A"
UP_TWO = "\033[2A"
REPLY_TO_RIGHT = "\033[6C"  # Pana la sfasit de linie
LEFT = "\033[1000D"  # Pana la inceput de linie
DOWN = "\033[1000B"  # Moves cursor 1000 positions down
HOME = "\033[H"
END_OF_LINE = "\033[(224;79)"
NEW_LINE = "\n"


def clear_line_above():
    print(f"{UP_ONE}{CLEAR_LINE}")


def clear_display():
    print(f"{CLEAR_DISPLAY}")


def socket_Alive(someSocket):
    try:
        if someSocket is not None:
            return True
    except Exp:
        pass
    return False


if socket_Alive(clientSocket):
    append_new_line(fisierLog, "Chat Began:" + currentTime + " with " + str(clientAddress))
    clear_display()


def receiveMessage(connection):
    """
    Function for all data

    :param socket: socket socket
    :return: received data
    """
    data = list()
    while True:
        message = connection.recv(100)
        data.append(message.decode())
        if message:
            return "".join(data)
        else:
            break


def message_From_Client():
    while socket_Alive(sock):
        # quitThread = quit_Queue.get()
        if socket_Alive(clientSocket):
            messageReceived = receiveMessage(clientSocket)
            print(f"{DOWN}{NEW_LINE}{UP_ONE}{BLUE}{messageReceived}{WHITE}{CLEAR_LINE}", end=f'{NEW_LINE}Reply:')
            if messageReceived == "-qq" or messageReceived == None:
                break
        elif socket_Alive(clientSocket) is not True:
            print("S-a pierdut conexiunea")
            break


def send_Message():
    while socket_Alive(sock):
        if socket_Alive(clientSocket):
            serverID = "Server:"
            messageSend = input(f"{DOWN}Reply:")
            print(f"{UP_ONE}{RED}{serverID}{GREEN}{messageSend}{CLEAR_LINE}{WHITE}")
            if messageSend == "-qq":
                clientSocket.sendto(messageSend.encode(), clientAddress)
                print("Ai ales sa inchizi conexiunea!")
                break
            else:
                clientSocket.sendto((serverID.encode() + messageSend.encode()), clientAddress)
        elif socket_Alive(clientSocket) is not True:
            print("S-a pierdut Conexiunea")
            break

# threading.Thread(target = run, args =(lambda : stop_threads, ))


thread_Receive_Message = threading.Thread(target=message_From_Client, daemon=True)
thread_Send_Message = threading.Thread(target=send_Message, daemon=True)
thread_Send_Message.start()
thread_Receive_Message.start()
thread_Send_Message.join()
thread_Receive_Message.join()
clientSocket.close()
sock.close()
clientSocket.shutdown(socket.SHUT_RDWR)
sock.shutdown(socket.SHUT_RDWR)
quit()
