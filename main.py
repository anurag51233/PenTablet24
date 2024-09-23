import serial
import serial.tools.list_ports
import time
import threading
import keyboard
import math
import Coordinate
import pyautogui


# Global variables for thread communication
last_data_time = time.time()

rbuttonpress = False

# Scan for available ports
available_ports = serial.tools.list_ports.comports()
ser = serial.Serial()


data = ("[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15.52417, 0, 17.88854, 25.94224, 0, 0, 0, 15.49193, 0, 41.0]")
# Convert the string to an actual list
coo = Coordinate.Coordinate()
ref1 = coo.calc(data)
print(ref1)


posx_move_old = 100
posy_move_old = 350

def process_data(data):
    global last_data_time
    global posx_move_old
    global posy_move_old
    last_data_time = time.time()  # Update last data time

    # ... (rest of your data processing and mouse control code)



    #print(f"Received from Arduino: {data}")

    ref1 = coo.calc(data)

    #if ref1[2] < 0.1:
    #     pyautogui.mouseDown(button='left')
         # rbuttonpress = True
    #else:
        # if rbuttonpress:
    #    pyautogui.mouseUp(button='left')
         # rbuttonpress = False

    #print(ref1)
    speed = 10


    posx_move = 100+ref1[0]*speed
    posy_move = 350+ref1[1]*speed



    if ((posx_move - posx_move_old)**2 + (posx_move - posx_move_old)**2) > 10:
        pyautogui.moveTo(posx_move, posy_move)  # Moves cursor to position (100, 150) i

    posx_move_old = 100 + ref1[0] * speed
    posy_move_old = 350 + ref1[1] * speed



# p = Plot()  # Uncomment if using the Plot class


if available_ports:
    for port in available_ports:
        if port.device == "COM3":
            print(f"Found port: {port.device}")

            try:
                # Connect to the first available port
                ser = serial.Serial(port.device, 9600, timeout=100)
                print(f"Connected to {ser.name}")

                while True:
                    try:
                        data = ser.readline().decode('latin-1').strip()
                        if len(data) > 0:
                            threading.Thread(target=process_data, args=(data,)).start()
                    except serial.SerialException as e:
                        print(f"Error reading from serial port: {e}")
                        break

                    # Check for user input and handle timeout
                    if keyboard.is_pressed('q') or time.time() - last_data_time > 5:
                        break

            except serial.SerialException as e:
                print(f"Error connecting to {port.device}: {e}")
            finally:
                if ser:
                    ser.close()
                    print("Serial connection closed.")
else:
    print("No serial ports found.")
