#!/usr/bin/python3

"""
    Author: C-Lock
    This is a python implementation of the desk_control script.
    In this code we construct a class with some methods, this lends itself to importing into other codes, like an API or something.
    Please note: The bt_addr in the main block of the code is unique to my desk. I'll try to remember to add a segment to the README about finding your own.

"""

import pygatt
from binascii import hexlify
import re
from time import sleep

class desk_controller:
    def __init__(self, bt_addr):
        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.bt_addr = bt_addr
        self.response_array=[]
        """
        response_array. I'm not clever. The callback function can mysteriously print data to the screen, but it cannot assign it to a variable.
        Response_array, however works. I can append the values to an array, and then use that array elsewhere.
        It's far from elegant, and it should DEFINITELY be fixed.
        """
        self.height=0
        actions = {
            'raise': [0xf1, 0xf1, 0x01, 0x00, 0x01, 0x7e], 
            'lower': [0xf1, 0xf1, 0x02, 0x00, 0x02, 0x7e], 
            'sit':   [0xf1, 0xf1, 0x05, 0x00, 0x05, 0x7e], 
            'stand': [0xf1, 0xf1, 0x06, 0x00, 0x06, 0x7e],
            'mon':   [0xf1, 0xf1, 0x07, 0x00, 0x07, 0x7e],
            'save1': [0xf1, 0xf1, 0x03, 0x00, 0x03, 0x7e],
            'save2': [0xf1, 0xf1, 0x04, 0x00, 0x04, 0x7e],
            #'save3': [0xf1, 0xf1, 0x07, 0x00, 0x07, 0x7e],
            'stop':  [0xf1, 0xf1, 0x07, 0x00, 0x07, 0x7e],
            }
        # For the curious: YES, I could hardcode this, however I wanted to preserve how to translate the data from the bluetooth sniffing into actions.
        # The data comes from the bluetooth in this strange format I haven't deciphered yet. Similarly, we must send data in that format.
        self.commands = {}
        for action in actions.keys():
            self.commands[action] = bytearray(actions[action])

    def bt_connect(self):
        """
        The pygatt tool is great, however we do experience *frequent* disconnects and connection failures.
        This method will attempt to establish a connection 5 times before failing out. 
        """
        attempts=0
        while attempts < 5:
            try:
                self.device=self.adapter.connect(self.bt_addr)
                self.device.subscribe("0000ff02-0000-1000-8000-00805f9b34fb", callback=self.handle_data) #This is how we retreive data!
            except pygatt.exceptions.NotConnectedError:
                attempts+=1
            else:
                return 0
        return 1

        
    def handle_data(self,handle, value): #callback function. Annoying to work with.
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        hex_bytes=hexlify(value)                #object of bytes to a byte-object of hex
        hex_string=hex_bytes.decode("utf-8")    #bytearray into string
        self.response_array.append(hex_string)  
        #print(hex_bytes)
        return hex_string

    def return_height(self,packet_data:list) -> float: 
        """
        intakes the data portion of a response packet, converts it to cm
        """
        sans_headers=packet_data[8:16]           #peel off the packet headers and keep the data
        hex_array=re.findall('..',sans_headers)  #split into an array of hex values
        dec_data=[]                                 
        if hex_array[0] == '01':                 #First hex is either 00 or 01, and is a yes/no for 256
            dec_data.append(256)
        else:
            dec_data.append(0)
        for val in hex_array[1:]:                #convert each value to decimal, add it to the array
            dec_data.append(int(val,16))
        #print(packet_data)
        return (dec_data[0]+dec_data[1])/4       #return the height in cm

    def send_command(self,action,reps=1):
        """
        Handles the actual writing of the data to the bluetooth handle
        """
        self.response_array=[]
        command=self.commands[action]
        while reps > 0:
            self.device.char_write_handle(0x0025,command)
            reps-=1
            sleep(.1)
        array_len0=len(self.response_array)
        sleep(5)
        while len(self.response_array) > array_len0: #The response values arrive asynchronosly, in the background. The main process threads on (DO NOT PARDON THAT PUN)
            #print(array_len0)                        #This loop tries (and fails) to ensure the responses have stopped arriving before we grab the final height
            array_len0=len(self.response_array)
            sleep(2)
        if len(self.response_array):
            self.height=self.return_height(self.response_array[-1]) #Use the final response to gauge height
            #print(self.height)
            return self.height
        
            
    def adjust_desk(self,action,reps=1):
        """
        Due to the frequent disconnects referenced in bt_connect(), we want to make sure we're connected.
        This function attempts to send_command(), however will try reconnecting once* if it errors out.
        """
        try: 
            self.send_command(action,reps)
        except:
            self.bt_connect() #remember, this is 5 attempts to reconnect.
            self.send_command(action,reps)


if __name__ == "__main__":
    from sys import argv
    bt_addr='34:e3:1a:12:A5:D3' # <------ REPLACE ME!
    action = argv[1]
    if len(argv) > 2 and action == 'raise' or action == 'lower':
        reps=int(argv[2])
    else:
        reps=1
    controller = desk_controller(bt_addr)
    controller.bt_connect()
    controller.adjust_desk(action,reps)
    #if action == 'mon':
    print(f"{controller.height}cm")

"""
#  gatttool -b $1 --char-write-req -a 0x0025 -n f1f10200027e
#handle='0x0025'
value='f1f10700077e'
up='f1f10100017e' #or 'f1f10700077e']
noaction='f1f12b002b7e'
down='f1f10200027e'

step_1="f1f10500057e"
step_2= "f1f10600067e"

"""
