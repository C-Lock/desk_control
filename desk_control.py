#!/usr/bin/python3

"""
    Author: C-Lock
    This is a python implementation of the desk_control script.
    In this code we construct a class with some methods, this lends itself to importing into other codes, like an API or something.
    Please note: The bt_addr in the main block of the code is unique to my desk. I'll try to remember to add a segment to the README about finding your own.

"""

import pygatt

class desk_controller:
    def __init__(self, bt_addr):
        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.bt_addr = bt_addr
        actions = {'raise':[0xf1, 0xf1, 0x01, 0x00, 0x01, 0x7e], 'lower': [0xf1,0xf1, 0x02, 0x00, 0x02, 0x7e], 'sit':[0xf1, 0xf1, 0x05, 0x00,0x05, 0x7e], 'stand':[0xf1,0xf1,0x06,0x00,0x06,0x7e]}
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
            except pygatt.exceptions.NotConnectedError:
                attempts+=1
            else:
                return 0
        return 1

    def send_command(self,action,reps=1):
        """
        Handles the actual writing of the data to the bluetooth handle
        """
        command=self.commands[action]
        while reps > 0:
            self.device.char_write_handle(0x0025,command)
            reps-=1
            
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
    if action == 'raise' or action == 'lower':
        reps=int(argv[2])
    else:
        reps=1
    controller = desk_controller(bt_addr)
    controller.adjust_desk(action,reps)

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
