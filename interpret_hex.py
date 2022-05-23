import json


def strip_value(notification): 
    """
    returns the 4 data carrying bits from the notification packet
    """
    hex=notification.split("f2 f2 01 03 ")[1]
    hex=hex.split(" ")[:4]
    return hex

def to_decimal(packet_data):
    """
    returns the 4 data bits converted into decimal (with appropriate modification)
    """
    dec_data=[]
    if packet_data[0] == '01':
        dec_data.append(256)
    else:
        dec_data.append(0)
    for val in packet_data[1:]:
        dec_data.append(int(val,16))
    return dec_data

def math_it(dec_data):
    """
    returns tuple with the following format
    (expected measurement, (x), unknown important value)
    where (x) is a placeholder.
    """
    return [(dec_data[0] + dec_data[1]), '(x)', dec_data[3]]

def alltogethernow(packet_data,dec_data,mathed):
    """
    returns a cool string.
    """
    return f"{packet_data} -> {dec_data} -> {mathed} -> {mathed[0]/4} {mathed[2]/4}"




if __name__ == "__main__":
    height_diff_array=[]
    with open("/home/creston/code/desk_control/measured_delta.json","r") as data_file:
        data_data=json.load(data_file)
    for value in data_data["values"]:
        value["Measured"] = float(value["Measured"])                                                        #Measured height (not from floor)
        value["App_Data"] = float(value["App_Data"])                                                        #App provided height
        value["packet_data"] = strip_value(value["notif"])                                                  #Data carrying bits
        value["dec_data"] = to_decimal(value["packet_data"])                                                #Data bits in decimal
        value["mathed"] = math_it(value["dec_data"])                                                        #(height from blt, (x), number) NOTE: mathed[0] is not yet converted to cm. must divide by 4.
        value["bluetooth"] = float(value['mathed'][0])/400                                                  #Height as calculated by the notification
        value["final_string"] = alltogethernow(value["packet_data"],value["dec_data"],value["mathed"])      #just some stuff
        value["app_diff"] = (value["App_Data"] - float(value["mathed"][0])/4)                               #Difference of the app provided height and the blt provided height.
        value["measured_diff"] = round(float(value["mathed"][0])/400 - value["Measured"],3)                 #Difference of the measured height and the blt provided height.
                                                                                                            #   *This is used to provide a constant "actual height" modifier. i.e. measured height + measured_diff = actual height from ground
                                                                                                            #   *This is required because the measured height is not from ground    
        height_diff_array.append(value["measured_diff"])                                                    # We add the measured diff to an array to get the average difference, to ensure that our calculated prediction is correct on average.
    for value in data_data["values"]:
        value["calculation"] = round(value["bluetooth"] - (sum(height_diff_array)/len(height_diff_array))/100,3)
        
        print(value["notif"])
        print(f"conversion: {value['final_string']}")
        print(f"App Data  : {value['App_Data']/100}m (-{value['app_diff']/100}m)")
        print(f"Measured  : {value['Measured']}m (+{value['measured_diff']}m)")
        print(f"Bluetooth : {value['bluetooth']}m")
        print(f"Calculated: {value['calculation']}m")
        print("\n\n")




#test_string="Notification handle = 0x0028 value: f2 f2 01 03 01 84 03 8c 7e"
#provide_answer(test_string)

#if __name__ == "__main__":
#    height_diff_array=[5.41]
#    while True:
#        notif_string=input("Provide Notification String: ")
#        app_height=float(input("Provide height yielded by app: "))
#        measured_height=float(input("Provide Accurate height from measurement: "))
#
#        provide_answer(notif_string,app_height,measured_height,height_diff_array)

