import socket
import serial
import glob
import RPi.GPIO as GPIO
from socket import error as SocketError
import errno


CheckWord = "chc"
StopWord = "Stop"


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


def save_pos(CamPos1, CamPos2):
    CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
    f = open('/nserver/cam_pos.conf', 'w')
    f.write(CamPos1 + "\n" + CamPos2)
    f.close()


def load_pos():
        f = open('/nserver/cam_pos.conf', 'r')
        pos = f.read()
        list_of_pos = pos.split('\n')
        CamPos1 = (int)list_of_pos[0]
        CamPos2 = (int)list_of_pos[1]
        return CamPos1, CamPos2


def init_arduino():
    try:
        CamPos1, CamPos2 = load_pos()
    except:
        CamPos1 = 500
        CamPos2 = 800
    try:
        dev = glob.glob('/dev/ttyACM*')[0]
    except:
        dev = 0
    print(dev)
    try:
        SerialArduino = serial.Serial(dev, 9600, timeout=1)
        camera_rotate(SerialArduino, CamPos1, CamPos2)
        ArduOnLine = True
        print("Arduino is online")
    except:
        ArduOnLine = False
        print("Arduino is offline. Check power, port and connection")
    return SerialArduino, ArduOnLine, CamPos1, CamPos2


def camera_pos_constrain(CamPos1, CamPos2):
    if CamPos1 > 900:
        CamPos1 = 900
    if CamPos1 < 100:
        CamPos1 = 100
    if CamPos2 > 970:
        CamPos2 = 970
    if CamPos2 < 400:
        CamPos2 = 400
    return CamPos1, CamPos2


def camera_rotate(SerialArduino, CamPos1, CamPos2):
    SerialArduino.write("Cam_Orient_(first,second) " + str(CamPos1) + " " + str(CamPos2) + "\n")

def socket_init():
    ServerPort = 8082
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created. Setting the socket...")
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Done. Binding the port...")
    sock.bind(("", ServerPort))
    print("Port has been binded. Starting listening...")
    sock.listen(1)
    print("Listening done. Retrieving conn and addr...")
    print("Done!")
    return sock


def main(SerialArduino, ArduOnLine, CamPos1, CamPos2):
    if not ArduOnLine:
        print("Arduino not connected. Shutting down...")
        exit(1)
    try:
        conn, addr = socket_init().accept()
        while True:
            data = conn.recv(1024)
            #print(data.decode())
            #if not data:
            #   break
            if data.decode == "" or data.decode == 0 or data.decode() == None:
                continue
            if data.decode() == CheckWord:
                print("I am OK")
                continue
            if data.decode() == StopWord:
                conn.send("Server turned off".encode())
                print("Shutdown server...")
                conn.close()
                exit(1)
            if data.decode() == "up":
                CamPos2 -= 10
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned up")
                continue
            if data.decode() == "up2":
                CamPos2 -= 50
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned up 2")
                continue
            if data.decode() == "up3":
                CamPos2 -= 100
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned up 3")
                continue
            if data.decode() == "down":
                CamPos2 += 10
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned down")
                continue
            if data.decode() == "down2":
                CamPos2 += 50
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned down 2")
                continue
            if data.decode() == "down3":
                CamPos2 += 100
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned down 3")
                continue
            if data.decode() == "left":
                CamPos1 += 10
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned left")
                continue
            if data.decode() == "left2":
                CamPos1 += 50
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned left 2")
                continue
            if data.decode() == "left3":
                CamPos1 += 100
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned left 3")
                continue
            if data.decode() == "right":
                CamPos1 -= 10
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned right")
                continue
            if data.decode() == "right2":
                CamPos1 -= 50
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned right 2")
                continue
            if data.decode() == "right3":
                CamPos1 -= 50
                CamPos1, CamPos2 = camera_pos_constrain(CamPos1, CamPos2)
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Turned right 3")
                continue
            if data.decode() == "center":
                CamPos1 = 500
                CamPos2 = 800
                camera_rotate(SerialArduino, CamPos1, CamPos2)
                print("Centered")
                continue
            if data.decode() == "disconnect":
                print("Client disconnected by demand")
                print("Restarting sockets...")
                conn.close()
                print("Connection closed. Initializing socket...")
                conn, addr = socket_init().accept()
                continue
            if data.decode() == "save_pos":
                print("Recieved comm for save")
                save_pos(CamPos1, CamPos2)
                conn.send("Position has been saved".encode())
                continue
            if data.decode() == "load_pos":
                print("Recieved comm for load")
                try:
                    load_pos(CamPos1, CamPos2)
                    camera_rotate(SerialArduino, CamPos1, CamPos2)
                    conn.send("Position has been loaded".encode())
                except:
                    conn.send("Load error".encode())
                continue
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
        print("Restarting sockets...")
        conn.close()
        main(SerialArduino, ArduOnLine, CamPos1, CamPos2)

SerialArduino, ArduOnLine, CamPos1, CamPos2 = init_arduino()
main(SerialArduino, ArduOnLine, CamPos1, CamPos2)