import serial,time

    
print('Running. Press CTRL-C to exit.')
with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
    time.sleep(0.1) #wait for serial to open
if arduino.isOpen():    
    print("{} connected!".format(arduino.port))
    try:        
        while True:
            cmd=input(1)
            arduino.write(cmd.encode())
    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
