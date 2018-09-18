'''
TODO add comments
add more clear reason for exceptions
check for exceptions of file read/write, so I shouldn't care about them in main.py
create method "move", which recieves just a direction and power
'''

import serial
import glob
import time


class Camera:
    def __init__(self):
        try:
            self.dev = glob.glob('/dev/ttyACM*')[0]
        except:
            self.dev = 0
        print(self.dev)
        try:
            self.arduino = serial.Serial(self.dev, 9600, timeout=1)
            self.connection_state = True
            print("Arduino is connected")
            time.sleep(5)
        except:
            self.connection_state = False
            print("Arduino is disconnected. Check power, port and connection")
        try:
            self.camera_pos_1, self.camera_pos_2 = self.load()
            print("Loaded pos: " + str(self.camera_pos_1) + " and " + str(self.camera_pos_2))
        except:
            print("Failed to load saved position of camera at boot. Try to do it manually")
            print("Using default values 500 and 800")
            self.camera_pos_1 = 500
            self.camera_pos_2 = 800
        self.rotate(self.camera_pos_1, self.camera_pos_2)

    def load(self):
        file = open('/nserver/cam_pos.conf', 'r')
        data = file.read()
        file.close()
        list_of_pos = data.split('\n')
        position_1 = int(list_of_pos[0])
        position_2 = int(list_of_pos[1])
        position_1, position_2 = self.constrain(position_1, position_2)
        return position_1, position_2

    def save(self):
        file = open('/nserver/cam_pos.conf', 'w')
        file.write(str(self.camera_pos_1) + "\n" + str(self.camera_pos_2))
        file.close()

    def rotate(self, position_1, position_2):
        position_1, position_2 = self.constrain(position_1, position_2)
        self.arduino.write("Cam_Orient_(first,second) " + str(position_1) + " " + str(position_2) + "\n")

    @staticmethod
    def constrain(position_1, position_2):
        if position_1 > 900:
            position_1 = 900
        if position_1 < 100:
            position_1 = 100
        if position_2 > 970:
            position_2 = 970
        if position_2 < 400:
            position_2 = 400
        return position_1, position_2

    def state(self):
        return self.connection_state

    def up(self, power):
        if power == 1:
            self.camera_pos_1 -= 10
        elif power == 2:
            self.camera_pos_1 -= 50
        elif power == 3:
            self.camera_pos_1 -= 100
        else:
            self.camera_pos_1 -= 10
        self.camera_pos_1, self.camera_pos_2 = self.constrain(self.camera_pos_1, self.camera_pos_2)
        self.rotate(self.camera_pos_1, self.camera_pos_2)

    def down(self, power):
        if power == 1:
            self.camera_pos_1 += 10
        elif power == 2:
            self.camera_pos_1 += 50
        elif power == 3:
            self.camera_pos_1 += 100
        else:
            self.camera_pos_1 += 10
        self.camera_pos_1, self.camera_pos_2 = self.constrain(self.camera_pos_1, self.camera_pos_2)
        self.rotate(self.camera_pos_1, self.camera_pos_2)

    def left(self, power):
        if power == 1:
            self.camera_pos_2 += 10
        elif power == 2:
            self.camera_pos_2 += 50
        elif power == 2:
            self.camera_pos_2 += 100
        else:
            self.camera_pos_2 += 10
        self.camera_pos_1, self.camera_pos_2 = self.constrain(self.camera_pos_1, self.camera_pos_2)
        self.rotate(self.camera_pos_1, self.camera_pos_2)

    def right(self, power):
        if power == 1:
            self.camera_pos_2 -= 10
        elif power == 2:
            self.camera_pos_2 -= 50
        elif power == 2:
            self.camera_pos_2 -= 100
        else:
            self.camera_pos_2 -= 10
        self.camera_pos_1, self.camera_pos_2 = self.constrain(self.camera_pos_1, self.camera_pos_2)
        self.rotate(self.camera_pos_1, self.camera_pos_2)

    def center(self):
        self.camera_pos_1 = 500
        self.camera_pos_2 = 800
        self.rotate(self.camera_pos_1, self.camera_pos_2)
