import os
import serial
import time
import pandas as pd
import numpy as np
import struct
from PyQt5 import QtGui
from PyQt5.QtWidgets import QInputDialog

# command <=0, label>0 
# command codes: start=0, stop=-1, pause=-2, resume=-3, label=1 

def send_label(ser,com_code):
    ser.write(bytes(com_code, 'utf-8')) 
 
def get_sample_rate(ser):
    timer_interval = int.from_bytes(ser.read(4), byteorder='little')
    return float(1000/timer_interval)

def time_linspace(st_time, sp_time, fs, time_interval):
    interval = 1000/fs
    return np.linspace(st_time, sp_time-interval, int(fs*time_interval)).astype(int)
 
def merge_data_and_time(df, df_prot, data_t_l, fs, counter, ind):
    time_interval = df_prot['time_interval'][ind]
    st=counter; sp=counter+int(fs*time_interval)-1
    df.loc[st:sp,'time_millisec'] = time_linspace(data_t_l[ind,0], data_t_l[ind+1,0], fs, time_interval)
    df.loc[st:sp,'label'] = data_t_l[ind][-1]
    counter += int(fs)*df_prot['time_interval'][ind]
    return counter

def replace_image_by_label(obj_gui, df_prot, indx):
    path_image = df_prot['path_image'][indx]
    obj_gui.motion_pic.setPixmap(QtGui.QPixmap(path_image))
    obj_gui.motion_pic.repaint()

def receive_data(ser, df_protocol, obj_gui):
    channels_opt = 8
    channels_imu = 9
 
    sample = True
    last = df_protocol.shape[0]
    df_protocol.loc[last] = ['stop', -1, df_protocol.loc[0,'time_interval'], df_protocol.loc[0,'path_image']]
    labels = df_protocol['label_index'].tolist()
    label_interval = df_protocol['time_interval'].tolist()
    
    send_label(ser, "0") # start signal
    replace_image_by_label(obj_gui, df_protocol, 0)
    print('Start recording')
    preamb = int.from_bytes(ser.read(4), byteorder='little')
    # print(preamb)
    start_time=0; label_id=0;
    if preamb==2857740885:       
        timer_id = int.from_bytes(ser.read(4), byteorder='little') 
        # print('timer_id: ', timer_id) 
        if timer_id==7: 
            start_time = int(int.from_bytes(ser.read(8), byteorder='little')/1000)
            time_millisec = 0
            label_id = int.from_bytes(ser.read(4), byteorder='little')
            fs0 = get_sample_rate(ser)
            fs1 = get_sample_rate(ser)
            print('sample rates: {}, {}'.format(fs0, fs1))
        else:
            print('error: timer_id')
            return           
    else:
        print('error: preambula')
        return

    #----------------------------
    duration = df_protocol['time_interval'].sum()-df_protocol.loc[last,'time_interval']
    print('duration:' ,duration, 'len:', df_protocol.shape[0])
    data_opt = np.zeros((int(duration*fs0), channels_opt+2), dtype=int)
    data_imu = np.zeros((int(duration*fs1), channels_imu+2), dtype=float)
    data_time_label = np.zeros((df_protocol.shape[0], 2), dtype=int)

    counter1=0; counter2=0; count_lab=0; lab_ind=0; 
    send_label(ser, str(labels[lab_ind]))
    replace_image_by_label(obj_gui, df_protocol, lab_ind)
    lab_ind += 1
    while sample:
        preamb = int.from_bytes(ser.read(4), byteorder='little')
        if preamb==2857740885:
            timer_id = int.from_bytes(ser.read(4), byteorder='little')
            # print('timer_id: ', timer_id)            
            if timer_id==0:
                for opt_inx in range(channels_opt):
                    current = int.from_bytes(ser.read(4), byteorder='little', signed=True)
                    data_opt[counter1, opt_inx+1] = current              
                counter1 += 1
                count_lab += 1 

            elif timer_id==1:                  
                for imu_inx in range(channels_imu):
                    [current] = struct.unpack('f', ser.read(4))
                    data_imu[counter2, imu_inx+1] = current
                counter2 += 1

            elif timer_id==7: 
                time_millisec = int(int.from_bytes(ser.read(8), byteorder='little')/1000)
                time_millisec = time_millisec-start_time
                print('times: {}, counter1 {}, counter2 {}'.format(time_millisec, counter1, counter2))
                label_id = int.from_bytes(ser.read(4), byteorder='little')    
                data_time_label[lab_ind-1, :] = [time_millisec, label_id]

            if count_lab>=label_interval[lab_ind-1]*fs0:
                send_label(ser, str(labels[lab_ind]))
                # print('lab_ind:', lab_ind)
                replace_image_by_label(obj_gui, df_protocol, lab_ind)
                lab_ind += 1
                count_lab=0

        if lab_ind>=df_protocol.shape[0]: 
            send_label(ser, "-1") # stop signal
            replace_image_by_label(obj_gui, df_protocol, 0)
            interval = 1000/fs0
            time_millisec = time_millisec+int(interval*fs0*label_interval[lab_ind-1])
            print('times: {}, counter1 {}, counter2 {}'.format(time_millisec, counter1, counter2))
            data_time_label[lab_ind-1, :] = [time_millisec, label_id]             
            sample = False          

    #-------------------
    df_data_opt = pd.DataFrame(data_opt, columns = ['time_millisec','ch11','ch12','ch13','ch14','ch21','ch22','ch23','ch24', 'label'])
    df_data_imu = pd.DataFrame(data_imu, columns = ['time_millisec','Ax','Ay','Az','Gx','Gy','Gz','Mx','My','Mz', 'label'])
    contr=0; contr2=0;
    for i in range(data_time_label.shape[0]-1):
        contr = merge_data_and_time(df_data_opt, df_protocol, data_time_label, fs0, contr, i)
        contr2 = merge_data_and_time(df_data_imu, df_protocol, data_time_label, fs1, contr2, i)
    
    return df_data_opt, df_data_imu

def dump_data(df_data_opt, df_data_imu, obj_gui):
    print(df_data_opt.shape)
    print(df_data_imu.shape)
    df_data_opt.to_csv(obj_gui.path_opt, index=False)
    df_data_imu.to_csv(obj_gui.path_imu, index=False)
    print('data saved')

def save_recording_info_to_db(obj_gui):
    path_db = obj_gui.edt_db_path.text()+'DataBase.xlsx'
    print('path_db:',path_db)
    
    xls = pd.ExcelFile(path_db)
    frames = dict(zip(xls.sheet_names,range(len(xls.sheet_names))))
    if os.path.isfile(path_db) and os.access(path_db, os.R_OK):
        df=[]
        for sheet, frame in frames.items(): 
            df_cur= pd.read_excel(path_db, sheet_name=sheet, dtype={'subject': str})
            df.append(df_cur)    
        
        if len(df[0][df[0]['subject']==obj_gui.edt_patient.text()]['subject_name'])==0:
            df[0].loc[df[0].shape[0]] = [obj_gui.edt_patient.text(), 'unknown']
        
        path_info = obj_gui.path_opt.split('\\')
        # print( )   
        subject = obj_gui.edt_patient.text()
        trial_dir = path_info[-3]
        cur_dir = path_info[-2]
        record_name = (path_info[-1])[:-8] 
        protocol = obj_gui.combo_exp.currentText()
        place_opt = obj_gui.combo_opt.currentText()
        place_imu = obj_gui.combo_imu.currentText()
        limb = obj_gui.combo_limb.currentText()
        df[-1].loc[df[-1].shape[0]] = [subject,  trial_dir, cur_dir, record_name, place_opt, place_imu, protocol, limb]
        
        try:  
            writer = pd.ExcelWriter(path_db, engine='xlsxwriter')
            for sheet, frame in frames.items(): 
                df[frame].to_excel(writer, sheet_name = sheet, index=False)
            writer.save() 
            print('db saved')  
        except OSError:
            print('File is still open.')
    else:
        print('File is not exist.')

def collect_data(obj_gui):
    df_protocol = pd.read_csv('exp_protocols/'+obj_gui.combo_exp.currentText()+'.csv') 
    for port in serial.tools.list_ports.comports():
        port = port.device
    # print('port:', port)
    ser = serial.Serial(port=port, baudrate=115200, timeout=.1)
    df_opt, df_imu = receive_data(ser, df_protocol, obj_gui)
    dump_data(df_opt, df_imu, obj_gui)
