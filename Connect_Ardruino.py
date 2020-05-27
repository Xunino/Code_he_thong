import serial
import time
ser = serial.Serial('COM5', 9600)

def Connect(user_input=""):
    # user_input = input("\n Type on / off / quit : ")
    if user_input =="w": # check ok
        print("Ok")
        time.sleep(0.1) 
        ser.write(b'w') 
        Connect()
    elif user_input =="p": # Pass
        print("")
        time.sleep(0.1)
        ser.write(b'p')
        Connect()
    elif user_input =="f": # False
        print("")
        time.sleep(0.1)
        ser.write(b'f')
        Connect()
    elif user_input =="a": # ??
        print("")
        time.sleep(0.1)
        ser.write(b'a')
        Connect()
    else:
        pass

#loop runs if true
# running = True
# while running:
#     data = input("Nhập: ")
#     Connect(user_input=data)
#     if data == "quit":
#         break