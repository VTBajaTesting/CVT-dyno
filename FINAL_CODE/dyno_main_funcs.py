# Python code containing common functions to be called by other python scripts.
import smbus
import RPi.GPIO as GPIO
import time
import sys
from pathlib import Path
import csv
from scipy.interpolate import interp1d

MOS_pin = 33
DPDT_pin = 16
servo_pin = 12
kill_pin = 18
reset_pin = 22

def init_I2C():
    # This function initializes the I2C connection using the built-in SMBus library.
    # Returns the bus, using the default bus 1 on the RPi.
    # Call as:  bus = init_I2C()
    
    return smbus.SMBus(bus = 1)

def init_GPIO():
    # This function initializes all GPIO pins used on the RPi.
    # Pin numbers are assigned to corrrespond to the header on the PCB.
    # Returns the servo object to control engine throttle.
    # Call as:  servo = init_GPIO()

    # Set GPIO mode to board layout and turn off errors
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Setup all pins as inputs or outputs
    GPIO.setup(MOS_pin, GPIO.OUT)
    GPIO.setup(DPDT_pin, GPIO.OUT)
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setup(kill_pin, GPIO.OUT)
    GPIO.setup(reset_pin, GPIO.OUT)
    # Define all output initial values
    GPIO.output(MOS_pin, 0)
    GPIO.output(DPDT_pin, 0)
    GPIO.output(kill_pin, 0)
    GPIO.output(reset_pin, 0)
    # Start servo PWM signal
    servo = GPIO.PWM(servo_pin, 50)
    servo.start(11)
    return servo

def set_throttle(servo, val):
    # This function changes the throttle to val.  val must be between 0 and 100.
    # Returns the servo object.
    # Call as: servo = set_throttle(servo, val)

    if val >= 0 and val <= 100:
        # Map throttle value to servo limits
        duty = interp1d([0, 100], [11, 4])
        servo.ChangeDutyCycle(float(duty(val)))
    return servo

def reset_arduino():
    # This function is used to reset the arduino, and reset the hardware clock to zero.
    # This prevents clock rollover (after 70 min) from occurring during data collection.
    # No variables are returned.
    # Call as:  reset_arduino()

    GPIO.output(reset_pin, 1)
    # Delay to ensure reset has occurred
    time.sleep(.25)
    GPIO.output(reset_pin, 0)
    # Delay to allow the arduino to initialize
    time.sleep(1)

def get_cal_data():
    # This function opens the calibration file to obtain the current calibration values.
    # Returns the slope and intercept from the last run in the calibration file.
    # Call as: [cal_b, cal_m] = get_cal_data()

    f = open('/home/pi/Documents/DYNO/FINAL_CODE/cal_values.csv')
    csv_f = csv.reader(f)
    # Reassign values until last row is reached
    for row in csv_f:
        cal_m = float(row[0])
        cal_b = float(row[1])
    return cal_b, cal_m

def apply_brake():
    # This function sets the brake to apply continuously.
    # Use stop_brake() or release_brake() to stop brake application.
    # No variables are returned.
    # Call as: apply_brake()

    # Turn off actuator and set direction to retract
    GPIO.output(MOS_pin, 0)
    GPIO.output(DPDT_pin, 1)
    # Retract actuator
    GPIO.output(MOS_pin, 1)

def release_brake():
    # This function sets the brake to release continuously.
    # Actuator end stops will prevent over-extension.
    # No variables are returned.
    # Call as: release_brake()

    # Turn off actuator and set direction to extend
    GPIO.output(MOS_pin, 0)
    GPIO.output(DPDT_pin, 0)
    # Extend actuator
    GPIO.output(MOS_pin, 1)
    
def step_brake(time_move):
    # This function increments the brake for a specified time.
    # Use a positive input to apply the brake, negative to release.
    # No variables are returned.
    # Call as: step_brake(<time to move>)

    # Set direction for actuator
    if time_move >= 0:
        GPIO.output(MOS_pin, 0)
        GPIO.output(DPDT_pin, 1)
    else:
        GPIO.output(MOS_pin, 0)
        GPIO.output(DPDT_pin, 0)
    # Move actuator for specified time
    GPIO.output(MOS_pin, 1)
    time.sleep(abs(time_move))
    GPIO.output(MOS_pin, 0)

def read_temp(bus):
    # This function reads the rotor temperature from the IR temp sensor.
    # Returns the rotor temperature in degrees Celsius and a corresponding color.
    # The color may be used as a window background color.
    # Call as: [temp, colorhex] = read_temp(bus)

    # I2C address and register for sensor
    ir_add = 0x5a
    ir_reg = 0x07
    # Read the temperature and convert to correct units
    try:
        raw = bus.read_word_data(ir_add, ir_reg)
    except:
        raw = 0
    temp = raw*0.02-273.15
    color = interp1d([20, 200],[0, 255])
    if temp < 20:
        colorhex = "#%02x%02x%02x" % (0, 255, 0)
    elif temp > 200:
        colorhex = "#%02x%02x%02x" % (255, 0, 0)
    else:
        colorhex = "#%02x%02x%02x" % (int(color(temp)), 255-int(color(temp)), 0)
    return temp, colorhex

def E_STOP(servo, window):
    # Function to initiate emergency stop for system.
    # Inputs are the throttle servo and main window objects.
    # No variables are returned.
    # Call as: E_STOP(servo, root)

    global status
    status = 'EMERGENCY STOP'
    # Set throttle servo to idle position
    servo.ChangeDutyCycle(11)
    # Kill engine
    GPIO.output(kill_pin, 1)
    # Release brake
    GPIO.output(MOS_pin, 0)
    GPIO.output(DPDT_pin, 0)
    GPIO.output(MOS_pin, 1)
    # Wait for engine to stop
    time.sleep(15)
    window.quit()
    window.destroy()
    GPIO.cleanup()

def get_values(bus):
    # Function to call data points from the Arduino through I2C.
    # Checks transmission for errors and returns a flag if an error occurred.
    # Returns values and timeastamps for P_RPM, S_RPM, and ADC_RAW.
    # Call as: [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)

    arduino_add = 0x03
    arduino_reg = 0
    num_bytes = 20
    # Request data from the Arduino
    try:
        val = bus.read_i2c_block_data(arduino_add, arduino_reg, num_bytes)
    # Return an error if the Arduino does not acknowledge the request
    except:
        val = [0]*num_bytes
        val[0] = 1
    checksum = val[18]*256+val[19]
    # Compare checksum to check for errors
    if sum(val[0:18]) == checksum:
        error = 0
    else:
        error = 1
    # Concatenate bytes to reconstruct 16 and 32 bit values
    P_RPM = val[0]*256+val[1]
    P_time = val[2]*16777216+val[3]*65536+val[4]*256+val[5]
    S_RPM = val[6]*256+val[7]
    S_time = val[8]*16777216+val[9]*65536+val[10]*256+val[11]
    ADC_raw = val[12]*256+val[13]
    ADC_time = val[14]*16777216+val[15]*65536+val[16]*256+val[17]
    return P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error

def convert_ADC_raw_torque(ADC_log, cal_b, cal_m):
    # Function to convert raw ADC data to torque data using calibrated values.
    # Returns list of torque values with the same timestamps as the original data set.
    # Call as: TORQUE = convert_ADC_raw_torque(ADC_raw, cal_b, cal_m)

    TORQUE = (ADC_log-cal_b)/cal_m
    return TORQUE

def write_file(time_data, data, filename):
    # Function to save a data file on the mounted flash drive.
    # No variables are returned.
    # Call as: write_file(time_data, data, filename)

    # Define the file path
    directory = '/media/usb1/'
    file = Path(directory+filename+'.csv')
    num_data = len(data)
    # Write data by row
    open(str(file), 'a')
    with open(str(file), 'a') as dataFile:
        writer = csv.writer(dataFile, quoting = csv.QUOTE_NONE)
        line = 0
        while line < num_data:
            writer.writerow([time_data[line], data[line]])
            line = line+1
        dataFile.close




    
