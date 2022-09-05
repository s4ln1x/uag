#!/usr/bin/env python3

# This program is intended to provided a set of functions to move a lego mindstorm
# ev3 using the debian based distro ev3dev and was made for a Mexican school project
# at Universidad Autonoma de Guadalajara
#
# ev3dev info on: https://www.ev3dev.org/
# school info on: http://www.uag.mx/
#
# The lego functions are implemented thinking on the lego as a tank vehicule with
# a gripper in the front and two sensors of his back
#

# Packages
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from maze import Graph, dijkstra, shortest_path, selecPoint, desplazamiento, run, movements
import socket

HOST = "127.0.0.1"
#HOST = "192.168.43.138"
PORT = 65432

# Classes
class lego_tank():

    def __init__(self):

        try:
            self.tank_drive = MoveTank(OUTPUT_D, OUTPUT_A)
            self.sound = Sound()
            self.sound.speak("Ready to start")
            self.sound.speak("Waiting for orders my commander")
        except:
            self.tank_drive = False

        self.degrees = 1230
        print("Create the tank_drive")

    def right(self):
        print("Turning right")
        if self.tank_drive:
            self.tank_drive.on_for_degrees(50 , -50, 470)
        else:
            # We do not have outputs if we run this from our own computer
            pass

    def left(self):
        print("Turning left")
        if self.tank_drive:
            self.tank_drive.on_for_degrees(-50 , 50, 470)
        else:
            # We do not have outputs if we run this from our own computer
            pass

    def forward(self):
        print("I am moving forward")
        if self.tank_drive:
            self.tank_drive.on_for_degrees(50 , 50, self.degrees)
        else:
            # We do not have outputs if we run this from our own computer
            pass

    def backward(self):
        print("I am moving backwards")
        if self.tank_drive:
            self.tank_drive.on_for_degrees(50 , 50, (-1) * self.degrees)
        else:
            # We do not have outputs if we run this from our own computer
            pass

def server():
    """Server that waits for instructions

    """
    kill = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        lego = lego_tank()
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                for s in data.decode('utf-8').split():
                    if s == 'left':
                        lego.left()
                    elif s == 'right':
                        lego.right()
                    elif s == 'forward':
                        lego.forward()
                    elif s == 'backward':
                        lego.backward()
                    elif s == 'run':
                        commands = run(True)
                        for command in commands:
                            comando = command.decode('utf-8')
                            if comando == 'left':
                                lego.left()
                            elif comando == 'right':
                                lego.right()
                            elif comando == 'forward':
                                lego.forward()
                            elif comando == 'backward':
                                lego.backward()
                            elif comando == 'finish':
                                break
                        kill = True
                    elif s == 'finish':
                        break
                try:
                    if kill:
                        conn.sendall(b"kill")
                        break
                    else:
                        conn.sendall(b"done")
                except:
                    print("Connection finished")
                    break
            try:
                lego.sound.speak("I finished with my orders commander in chief")
            except:
                print("I finished with my orders commander in chief")


if "__main__"==__name__:
    server()
