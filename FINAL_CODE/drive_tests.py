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

def run_t1(p_speed: int, s_speed:[], torque_ratio, i_torque):
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
    def t1_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        #file_name = '/media/usb1/DYNODATA/drive/test1v'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'
        file_name = '/media/usb1/DYNODATA/drive/test1.csv'
        step_brake(-20)
        #assure initial conditions will be met
        speed_up_primary(p_speed, servo, bus)
        time.sleep(.500)
        torque_up(cal_m, cal_b, i_torque * torque_ratio, bus)
        time.sleep(.500)
        with open(file_name, 'w') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE\n')
            for s in s_speed:
                print(s)
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
    t1_backend(servo, bus, cal_m, cal_b)
    torque_up(cal_m, cal_b, 0, bus)
    speed_up_primary(0, servo, bus)
    speed_up_secondary(0, servo, bus)


def run_t2(i_torque:[],s_speed:[],torque_ratio):
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

    def t2_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        #file_name = '/media/usb1/DYNODATA/drive/test2v'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'
        file_name = '/media/usb1/DYNODATA/drive/test2.csv'
        step_brake(-20)
        #assure initial conditions will be met
        with open(file_name, 'w') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE\n')
            for t in i_torque:
                torque_up(cal_m, cal_b, t * torque_ratio, bus)
                time.sleep(.500)
                for s in s_speed:
                    speed_up_secondary(s,servo, bus)

                    #get all the data
                    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
                    
                    #find the torques
                    output_torque = convert_ADC_raw_torque(ADC_raw, cal_b, cal_m)
                    input_torque = output_torque / torque_ratio
                    f.write(str(P_RPM)+','+str(S_RPM)+','+str(input_torque)+','
                    +str(output_torque)+'\n')#need to add in variator ratio
                    #increment the speed
                    time.sleep(.500)
            f.close()
    t2_backend(servo, bus, cal_m, cal_b)
    torque_up(cal_m, cal_b, 0, bus)
    speed_up_primary(0, servo, bus)
    speed_up_secondary(0, servo, bus)

def run_t3(o_torque:[], s_speed:[], torque_ratio):
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

    def t3_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        #file_name = '/media/usb1/DYNODATA/drive/test3v'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'
        file_name = '/media/usb1/DYNODATA/drive/test3.csv'
        step_brake(-20)
        #assure initial conditions will be met
        time.sleep(.500)
        with open(file_name, 'w') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE\n')
            for t in o_torque:
                torque_up(cal_m, cal_b, t, bus)
                time.sleep(.500)
                for s in s_speed:
                    speed_up_secondary(s, servo, bus)
                    #get all the data
                    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
                    
                    #find the torques
                    output_torque = convert_ADC_raw_torque(ADC_raw, cal_b, cal_m)
                    input_torque = output_torque / torque_ratio
                    f.write(str(P_RPM)+','+str(S_RPM)+','+str(input_torque)+','
                    +str(output_torque)+'\n')#need to add in variator ratio
                    #increment the speed
            f.close()
    t3_backend(servo, bus, cal_m, cal_b)
    torque_up(cal_m, cal_b, 0, bus)
    speed_up_primary(0, servo, bus)
    speed_up_secondary(0, servo, bus)

def run_t4(i_torque:[], p_speed:[] ,torque_ratio):
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

    def t4_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        #file_name = '/media/usb1/DYNODATA/drive/test3v'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'
        file_name = '/media/usb1/DYNODATA/drive/test3.csv'
        step_brake(-20)
        #assure initial conditions will be met
        time.sleep(.500)
        with open(file_name, 'w') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE\n')
            for t in i_torque:
                torque_up(cal_m, cal_b, t * torque_ratio, bus)
                time.sleep(.500)
                for s in p_speed:
                    speed_up_primary(s, servo, bus)
                    #get all the data
                    [P_time, P_RPM, S_time, S_RPM, ADC_time, ADC_raw, error] = get_values(bus)
                    
                    #find the torques
                    output_torque = convert_ADC_raw_torque(ADC_raw, cal_b, cal_m)
                    input_torque = output_torque / torque_ratio
                    f.write(str(P_RPM)+','+str(S_RPM)+','+str(input_torque)+','
                    +str(output_torque)+'\n')#need to add in variator ratio
                    #increment the speed
            f.close()
    t4_backend(servo, bus, cal_m, cal_b)
    torque_up(cal_m, cal_b, 0, bus)
    speed_up_primary(0, servo, bus)
    speed_up_secondary(0, servo, bus)

def run_custom_john(i_torque:[], i_speed ,torque_ratio):
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

    def john_backend(servo, bus, cal_m, cal_b):
        #save in a folder with all the other drive tests
        #file_name = '/media/usb1/DYNODATA/drive/testjohnv'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv'
        file_name = '/media/usb1/DYNODATA/drive/testjohn.csv'
        step_brake(-20)
        #assure initial conditions will be met
        time.sleep(.500)
        speed_up_primary(i_speed, servo, bus)
        with open(file_name, 'w') as f:
            f.write('P_RPM,S_RPM,INPUT_TORQUE,OUTPUT_TORQUE\n')
            for t in i_torque:
                torque_up(cal_m, cal_b, t * torque_ratio, bus)
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
    john_backend(servo, bus, cal_m, cal_b)
    torque_up(cal_m, cal_b, 0, bus)
    speed_up_primary(0, servo, bus)
    speed_up_secondary(0, servo, bus)
            