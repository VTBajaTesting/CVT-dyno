from dyno_main_funcs import *
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

def run_t5(p_speed: [], i_torque:[], torque_ratio):
    cal_b, cal_m = get_cal_data()
    P_RPM = 0
    S_RPM = 0
    ADC_raw = 0
    P_time = 0
    S_time = 0
    ADC_time = 0
    error = 0
    servo = init_GPIO()
    bus = init_I2C()
    complete = 0
    def t5_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        #file_name = '/media/usb1/DYNODATA/drive/test5v'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'
        file_name = '/media/usb1/DYNODATA/coast/test5.csv'
        step_brake(-20)
        #assure initial conditions will be met
        with open(file_name, 'w') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE\n')
            for t in i_torque:
                torque_up(cal_m, cal_b,t * torque_ratio, bus)
                time.sleep(.500)
                for s in p_speed:
                    speed_up_primary(s,servo,bus)
                    time.sleep(.500)
                    #get all the data
                    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
                    
                    #find the torques
                    output_torque = convert_ADC_raw_torque(ADC_raw, cal_b, cal_m)
                    input_torque = output_torque / torque_ratio
                    f.write(str(P_RPM)+','+str(S_RPM)+','+str(input_torque)+','
                    +str(output_torque)+'\n')#need to add in variator ratio
                    #increment the speed

            f.close()
    t5_backend(servo, bus, cal_m, cal_b)
    torque_up(cal_m, cal_b, 0, bus)
    speed_up_primary(0, servo, bus)
    speed_up_secondary(0, servo, bus)

def run_t6(s_speed: int, o_torque:[], torque_ratio):
    cal_b, cal_m = get_cal_data()
    P_RPM = 0
    S_RPM = 0
    ADC_raw = 0
    P_time = 0
    S_time = 0
    ADC_time = 0
    error = 0
    servo = init_GPIO()
    bus = init_I2C()
    complete = 0
    def t6_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        #file_name = '/media/usb1/DYNODATA/drive/test5v'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'
        file_name = '/media/usb1/DYNODATA/coast/test6.csv'
        step_brake(-20)
        #assure initial conditions will be met
        with open(file_name, 'w') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE\n')
            for t in o_torque:
                torque_up(cal_m, cal_b,t, bus)
                time.sleep(.500)
                for s in s_speed:
                    speed_up_secondary(s,servo,bus)
                    time.sleep(.500)
                    #get all the data
                    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
                    
                    #find the torques
                    output_torque = convert_ADC_raw_torque(ADC_raw, cal_b, cal_m)
                    input_torque = output_torque / torque_ratio
                    f.write(str(P_RPM)+','+str(S_RPM)+','+str(input_torque)+','
                    +str(output_torque)+'\n')#need to add in variator ratio
                    #increment the speed

            f.close()
    t6_backend(servo, bus, cal_m, cal_b)
    torque_up(cal_m, cal_b, 0, bus)
    speed_up_primary(0, servo, bus)
    speed_up_secondary(0, servo, bus)
