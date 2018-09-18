from CameraHandler import Camera
from SockHandler import Socket
from socket import error as SocketError
import errno

sock = Socket('', 8082)
camera = Camera()
if not camera.state():
    print("Arduino is disconnected. Exiting with code 0")
    exit(0)
while True:
    try:
        data = sock.receive()
        if data == "" or data == 0 or data == None:
            continue
        if data == "up":
            camera.up(1)
        elif data == "up2":
            camera.up(2)
        elif data == "up3":
            camera.up(3)
        elif data == "down":
            camera.down(1)
        elif data == "down2":
            camera.down(2)
        elif data == "down3":
            camera.down(3)
        elif data == "left":
            camera.left(1)
        elif data == "left2":
            camera.left(2)
        elif data == "left3":
            camera.left(3)
        elif data == "right":
            camera.right(1)
        elif data == "right2":
            camera.right(2)
        elif data == "right3":
            camera.right(3)
        elif data == "center":
            camera.center()
        elif data == "save_pos":
            camera.save()
        elif data == "load_pos":
            try:
                position_1, position_2 = camera.load()
                camera.rotate(position_1, position_2)
                sock.send("Position has been loaded")
            except:
                sock.send("Load error")
                continue
        elif data == "disconnect":
            sock.disconnect()
            sock = Socket('', 8082)
            continue
        else:
            print("Unknown data: " + str(data))
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
        print("Restarting sockets...")
        sock.disconnect()
        sock = Socket('', 8082)
        continue