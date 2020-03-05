from drive_tests import *
torque_ratio = float(input('what is the torque ratio'))
num_elem = input('how many secondary speeds?')
s_speed = []
for _ in range(int(num_elem)):
    s_speed.append(int(input('Enter speed')))
p_speed = int(input('Enter primary speed'))
i_torque = int(input('Enter input torque'))
run_t1(p_speed, s_speed, torque_ratio, i_torque)