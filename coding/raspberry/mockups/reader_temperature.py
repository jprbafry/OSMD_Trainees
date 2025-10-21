import serial #communication with arduino
import time #time delay
I


port = '/dev/ttyACM0' #arduino port. DOUBLE CHECK THIS!
baud = 9600 #arduino baudrate 
ser = serial.Serial(port, baud) #set up serial communication
time.sleep(2) #wait for arduino to initialize

print("Reading temperature data from Arduino...")



#Main loop

try:
    while True:
        if ser.in_waiting > 0: #check if data is available
            line = ser.readline().decode('utf-8', errors = 'replace').strip() #read a line and decode puts out ASCII text

            #Skip empty lines
            if not line:
                continue

            try:
                temp_str = line.split()[0] #get the temperature part
                temperature = float(temp_str) #convert to float
                print(f"Temperature: {temperature:.2f} °C") #print temperature with 2 decimal places
            
            except ValueError:
                print(f"Received invalid data: {line}") #If conversion fails, print the invalid data

        time.sleep(0.2) #small delay to avoid overwhelming the serial buffer

except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    ser.close() #close serial port
    print("Serial port closed.")
        