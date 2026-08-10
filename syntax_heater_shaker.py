import serial
import time
import traceback
import sys

COMPORT_SHAKER = 'COM5'
COMPORT_HEATER = 'COM8'


class Syntax_Heater_Shaker():

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.HS_type = "syntax"
        self.ventilation_valve = 1

        self.std_velocity = 1000
        self.increased_velocity = 1000 # may have to change
        self.std_acceleration = 1


    def send_command_to_shaker(self, command, delay_after_command):

        while (1):

            try:
                command = command + '\r'

                self.ser = serial.Serial(COMPORT_SHAKER)
                self.ser.write(bytes(command, 'utf-8'))
                time.sleep(delay_after_command)
                reply = self.ser.read(self.ser.in_waiting)
                #print(reply)
                self.ser.close()

                return reply

            except Exception:

                print("\033[91m{}\033[00m".format(traceback.format_exc()))
                print("\033[91m{}\033[00m".format("Error on the heater_shaker, raised in syntax_heater_shaker.py.Retry in 2s."))
                time.sleep(2)

    def startShaking(self, velocity=None, acceleration=None):

        if velocity is None:
            velocity = self.std_velocity
        if acceleration is None:
            acceleration = self.std_acceleration

        ''' Specific instructions to be able to use this class with a prototype without changing all programs'''
        if velocity == 900:
            velocity = self.std_velocity
        elif velocity == 1100:
            velocity = self.increased_velocity

        self.send_command_to_shaker('setShakeTargetSpeed' + str(velocity), 0.2)
        self.send_command_to_shaker('setShakeAcceleration' + str(acceleration), 0.2)
        self.send_command_to_shaker('shakeOn', acceleration + 1)

    def stopShaking(self, acceleration=None):

        if acceleration is None:
            acceleration = self.std_acceleration

        while(1):   #Error caught since the status bytes of the shaker can sometimes be corrupted, and not correspond to an int, throwing an error
                    #Example: msg_from_shaker = b'0/r/nu'
            try:
                shaker_status = int(self.send_command_to_shaker('getShakeState', 0.2))
                #print("shaker_status=" + str(shaker_status))
                break

            except Exception:
                print("\033[91m{}\033[00m".format(traceback.format_exc()))
                print("\033[91m{}\033[00m".format("Error on the status of heater_shaker, raised in syntax_heater_shaker.py.Retry in 2s."))
                time.sleep(2)

        if shaker_status == 0: #if the shaker is running
            self.send_command_to_shaker('shakeOff', acceleration + 3)

        else: #if it's not running, just goHome
            self.send_command_to_shaker('shakeGoHome', 3)

    def goHome(self):
        self.send_command_to_shaker('shakeGoHome', 3)

    def send_command_to_heater(self, command):

        while(1):

            try:
                command = command + '\r\n'

                self.ser = serial.Serial(COMPORT_HEATER)
                self.ser.write(bytes(command, 'utf-8'))
                #reply = self.ser.read(self.ser.in_waiting)
                #print(reply)
                self.ser.close()
                return

            except Exception:

                print("\033[91m{}\033[00m".format(traceback.format_exc()))
                print("\033[91m{}\033[00m".format("Error on the heater_shaker, raised in syntax_heater_shaker.py.Retry in 2s."))
                time.sleep(2)

    def open_vac(self):
        if self.ventilation_valve :
            self.close_vent_valve()
        self.open_vac_valve()

    def close_vac(self):
        self.close_vac_valve()
        if self.ventilation_valve :
            self.open_vent_valve()

    def open_vac_valve(self):
        self.send_command_to_heater('2500')

    def close_vac_valve(self):
        self.send_command_to_heater('3000')

    def open_vent_valve(self):
        self.send_command_to_heater('3500')

    def close_vent_valve(self):
        self.send_command_to_heater('4000')

    def startHeating(self):
        self.send_command_to_heater('1500')

    def stopHeating(self):
        self.send_command_to_heater('2000')


if __name__ == "__main__":
    # On crée la racine de notre interface
    parent = 'fake parent'
    arduinoControl = Syntax_Heater_Shaker(parent)

    arduinoControl.open_vent()

    command = sys.argv[1]

    if command == "startShaking":
        arduinoControl.startShaking()
    elif command == "stopShaking":
        arduinoControl.stopShaking()
    elif command == "startHeating":
        arduinoControl.startHeating()
    elif command == "stopHeating":
        arduinoControl.stopHeating()
    else:
        print("unknown command")
