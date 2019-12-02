from dyno_main_funcs import *
from tkinter import *
import time
import os
import smbus
import _thread
from torque_interp import *
P_RPM = 0
S_RPM = 0
ADC_raw = 0
P_time = 0
S_time = 0
ADC_time = 0
error = 0

complete = 0

sample_rate = 150.
log_period = 1/sample_rate

time_upshift = 15

cal_b = 0
cal_m = 0

status = 'INITIALIZING'
wait_status = 1

def run_t1(p_speed: int, s_speed:[], torque_ratio, i_torque):
    
    def t1_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        file_name = '/media/usb1/DYNODATA/drive/test1v'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'

        #assure initial conditions will be met
        speed_up_primary(p_speed, servo, bus)
        time.sleep(500)
        torque_up(cal_m, cal_b, i_torque * torque_ratio, bus)
        time.sleep(500)
        with open(file_name, 'wb') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE')
            for s in s_speed:
                #get all the data
                [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
                
                #find the torques
                output_torque = convert_ADC_raw_torque(ADC_raw, cal_b, cal_m)
                input_torque = output_torque / torque_ratio
                f.write(str(P_RPM)+','+str(S_RPM)+','+str(input_torque)+','
                +str(output_torque))#need to add in variator ratio
                #increment the speed
                speed_up_secondary(s,servo,bus)
                time.sleep(500)
        