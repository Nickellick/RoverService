from getkey import getkey, keys
import socket

rasp_ip = "192.168.0.61"
rasp_port = 8082
chc = "chc"
sock = socket.socket()

def connect_to_rpi(rasp_ip, rasp_port):
    try:
        sock.connect((rasp_ip, rasp_port))
        return "True"
    except ConnectionRefusedError:
        print("Server not found")
        return "False"

def send_data(data):
    sock.send(chc.encode())
    connectionState = sock.recv(1024).decode()
    if connectionState == "True":
        sock.send(data.encode())
        return
    else:
        print("Server was disconnected!")
        exit(1)
        return


def recv_data():
    dt = sock.recv(1024).decode()
    if dt == "Server turned off":
        sock.close()
        print(dt + " Exit? (y/n)")
        exst = input()
        if exst.upper() == "YES" or exst.upper() == "Y":
            exit(1)
    return dt


connectionState = connect_to_rpi(rasp_ip, rasp_port)
while True:
    if connectionState == "True":
        print("Ready for input")
        key = getkey()
        if key == "up":
            send_data("up")
            if connectionState == "True":
                data = recv_data()
                print(data)
            else:
                exit(1)
        if key == "down":
            send_data("down")
            if connectionState == "True":
                data = recv_data()
                print(data)
            else:
                exit(1)
        if key == "left":
            send_data("left")
            if connectionState == "True":
                data = recv_data()
                print(data)
            else:
                exit(1)
        if key == "right":
            send_data("right")
            if connectionState == "True":
                data = recv_data()
                print(data)
            else:
                exit(1)
        if key == "c":
            send_data("center")
            if connectionState == "True":
                data = recv_data()
                print(data)
            else:
                exit(1)
        else:
            # data = input()
            # send_data(data)
            send_data(key)
            if connectionState == "True":
                data = recv_data()
                print(data)
            else:
                exit(1)
        #sock.close()
    else:
        exit(1)