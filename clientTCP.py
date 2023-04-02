#!/usr/bin/env python3
import socket
import threading
from threading import Lock
import datetime
from queue import Queue
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ("127.0.0.1", 7777)  # schimbari variabila tuple
sock.connect(serverAddress)

quit_Queue = Queue(maxsize=1)

# ANSI escape codes:
WHITE = "\033[0m"
RED = "\033[38;2;255;25;25m"
BLUE = "\033[38;2;75;75;255m"
GREEN = "\033[38;2;60;255;60m"
CLEAR_DISPLAY = "\033[2J"
# Clears characters from cursor position until the end of line
CLEAR_LINE = "\033[K"
UP = "\033[1000A"  # Moves cursor 1000 positions up
UP_ONE = "\033[1A"
UP_TWO = "\033[2A"
DOWN = "\033[1000B"  # Moves cursor 1000 positions down
HOME = "\033[H"
END_OF_LINE = "\033[0;79"
NEW_LINE = "\n"


def clear_line_above():
    print(f"{UP_ONE}{CLEAR_LINE}")


def clear_display():
    print(f"{CLEAR_DISPLAY}")


clear_display()


def socket_Alive(someSocket):
    try:
        if someSocket is not None:
            return True
    except Exp:
        pass
    return False


def send_Message():
    while socket_Alive(sock):
        ClientID = "Razvan:"   
        messageSend = input(f"{DOWN}Reply:")
        print(f"{UP_ONE}{RED}{ClientID}{GREEN}{messageSend}{WHITE}{CLEAR_LINE}")
        if messageSend == "-qq":
            print("Ai ales sa inchizi conexiunea!")
            break
        elif messageSend != "-qq": 
            sock.sendto((ClientID.encode() + messageSend.encode()), serverAddress)
        elif socket_Alive(sock) is not True:
            print("S-a pierdut Conexiunea")
            break


def message_From_Server():
    while True:
        if socket_Alive(sock):
            messageReceived = sock.recv(100)
            print(f"{DOWN}{NEW_LINE}{UP_ONE}{BLUE}{messageReceived.decode()}{WHITE}{CLEAR_LINE}", end=f'{NEW_LINE}Reply')
        elif socket_Alive(sock) is not True: 
            print("S-a pierdut conexiunea")
            break
        if messageReceived == "-qq":
            break


thread_Receive_Message = threading.Thread(target=message_From_Server, daemon=True)
thread_Send_Message = threading.Thread(target=send_Message, daemon=True)
thread_Send_Message.start()
thread_Receive_Message.start()
thread_Send_Message.join()
thread_Receive_Message.join()
sock.close()
sock.shutdown(socket.SHUT_RDWR)
quit()