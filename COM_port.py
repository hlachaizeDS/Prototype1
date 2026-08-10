import pyTMCL
import serial
import serial.tools.list_ports
import time

def list_1161_coms_by_adress():
    ports = serial.tools.list_ports.comports()

    adress_to_ports_dict={}

    for port in ports:
        if port.vid==10812 and port.pid==256: #specifics to vendor and product of TMCM 1161
            try:
                card=serial.Serial(port.name)
                card.write(b'\x01\nB\x00\x00\x00\x00\x00M') #Ask for serial adress of the card
                rep = card.read(9)
                adress=int.from_bytes(rep[5:8],"big") #Read the value of the response = serial adress
                if adress in adress_to_ports_dict.keys():
                    raise NameError("Two cards have the same adress : " + str(adress) + " !!")
                else:
                    adress_to_ports_dict[adress]=port.name
            except:
                pass
    return adress_to_ports_dict

if __name__ == "__main__":
    start=time.time()
    print(list_1161_coms_by_adress())
    end=time.time()
    print(end-start)