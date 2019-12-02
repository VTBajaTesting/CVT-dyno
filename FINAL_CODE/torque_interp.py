from dyno_main_funcs import *
from scipy.interpolate import interp1d
import RPi.GPIO
import smbus
MOS_pin = 33
DPDT_pin = 16
servo_pin = 12
kill_pin = 18
reset_pin = 22
init_GPIO()

def torque_up(cal_m, cal_b, requested_torque, bus):
    """
    precondition: init_GPIO is called
    bus is an object made using init_I2C
    
    Takes 4 arguments:
    cal_m: slope of the torque calibration curve
    cal_b: y-intercept of the torque calibration curve
    requested_torque: the torque to speed up to
    bus: the i2c bus that the dyno reads data on

    Resets the OUTPUT torque to the specified value 
    """
    step_brake(-1)
    num_good = 0
    ADC_time_last = 0
    max_data = 10000
    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = [0,0,0,0,0,0,0]
    while convert_ADC_raw_torque(ADC_raw, cal_b, cal_m) < requested_torque and num_good < max_data:
        [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
        # Confirm transmission was successful and not a duplicate data point
        if error == 0 and not ADC_time == ADC_time_last:
            num_good = num_good+1
        step_brake(1)
        time.sleep(500)

def speed_up_primary(rpm, servo, bus):
    """
    precondition: init_GPIO is called
    bus is an object made using init_I2C
    servo is a PWM device

    rpm: the desired speed for the primary(input speed)
    servo:the servo that controls the throttle
    bus: the i2c bus that the dyno redas data from

    Sets the primary's speed/input speed to rpm
    """
    s=1
    ADC_last = 0
    set_throttle(servo, 0)
    time.sleep(500)
    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = [0,0,0,0,0,0,0]
    while(s < 100 and P_RPM < rpm):
        set_throttle(servo, s)
        time.sleep(500)
        [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
        s = s + 1

def speed_up_secondary(rpm, servo, bus):
    """
    precondition: init_GPIO is called
    bus is an object made using init_I2C
    servo is a PWM device

    rpm: the desired speed for the secondary(output speed)
    servo:the servo that controls the throttle
    bus: the i2c bus that the dyno redas data from

    Sets the secondary's speed/output speed to rpm
    """
    s=1
    ADC_last = 0
    set_throttle(servo, 0)
    time.sleep(500)
    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = [0,0,0,0,0,0,0]
    while(s < 100 and S_RPM < rpm):
        set_throttle(servo, s)
        time.sleep(500)
        [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
        s = s + 1
