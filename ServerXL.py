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


def initArduino():
    CamPos1 = 500
    CamPos2 = 800
    try:
        dev = glob.glob('/dev/ttyACM*')[0]
    except:
        dev = 0
    print(dev)
    try:
        SerialArduino = serial.Serial(dev, 9600, timeout=1)
        cameraRotate(SerialArduino, CamPos1, CamPos2)
        ArduOnLine = True
        print("Arduino is online")
    except:
        ArduOnLine = False
        print("Arduino is offline. Check power, port and connection")
    return SerialArduino, ArduOnLine, CamPos1, CamPos2


def cameraPosConstrain(CamPos1, CamPos2):
    if CamPos1 > 900:
        CamPos1 = 900
    if CamPos1 < 100:
        CamPos1 = 100
    if CamPos2 > 970:
        CamPos2 = 970
    if CamPos2 < 400:
        CamPos2 = 400
    return CamPos1, CamPos2


def cameraRotate(SerialArduino, CamPos1, CamPos2):
    CamPos1, CamPos2 = cameraPosConstrain(CamPos1, CamPos2)
    SerialArduino.write("Cam_Orient_(first,second) " + str(CamPos1) + " " + str(CamPos2) + "\n")

def initSocket():
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


def mainFunc(SerialArduino, ArduOnLine, CamPos1, CamPos2):
    if not ArduOnLine:
        print("Arduino not connected. Shutting down...")
        exit(1)
    try:
        conn, addr = initSocket().accept()
        while True:
            data = conn.recv(1024)
            #print(data.decode())
            #if not data:
            #   break
            if data.decode == "" or data.decode == 0 or data.decode() == None:
                continue
            if data.decode() == CheckWord:
                conn.send("True".encode())
                print("I am OK")
                continue
            if data.decode() == StopWord:
                conn.send("Server turned off".encode())
                print("Shutdown server...")
                conn.close()
                exit(1)
            if data.decode() == "up":
                CamPos2 -= 10
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned up")
                continue
            if data.decode() == "up2":
                CamPos2 -= 50
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned up 2")
                continue
            if data.decode() == "up3":
                CamPos2 -= 100
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned up 3")
                continue
            if data.decode() == "down":
                CamPos2 += 10
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned down")
                continue
            if data.decode() == "down2":
                CamPos2 += 50
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned down 2")
                continue
            if data.decode() == "down3":
                CamPos2 += 100
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned down 3")
                continue
            if data.decode() == "left":
                CamPos1 += 10
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned left")
                continue
            if data.decode() == "left2":
                CamPos1 += 50
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned left 2")
                continue
            if data.decode() == "left3":
                CamPos1 += 100
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned left 3")
                continue
            if data.decode() == "right":
                CamPos1 -= 10
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned right")
                continue
            if data.decode() == "right2":
                CamPos1 -= 50
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned right 2")
                continue
            if data.decode() == "right3":
                CamPos1 -= 50
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Turned right 3")
                continue
            if data.decode() == "center":
                CamPos1 = 500
                CamPos2 = 800
                cameraRotate(SerialArduino, CamPos1, CamPos2)
                conn.send("True".encode())
                print("Centered")
                continue
            if data.decode() == "disconnect":
                print("Client disconnected by demand")
                print("Restarting sockets...")
                conn.close()
                print("Connection closed. Initializing socket...")
                conn, addr = initSocket().accept()
                continue
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
        print("Restarting sockets...")
        conn.close()
        mainFunc(SerialArduino, ArduOnLine, CamPos1, CamPos2)

SerialArduino, ArduOnLine, CamPos1, CamPos2 = initArduino()
mainFunc(SerialArduino, ArduOnLine, CamPos1, CamPos2)