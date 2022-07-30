import tkinter as tk
from tkinter import ttk
import os
import csv
import serial
import math

class position_Info(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,width=360,height=480,borderwidth=4,relief='groove')
        self.master = master
        #self.grid(row=0,column=0,rowspan=2)
        self.pack()
        #self.pack_propagate(0)

        self.hh = tk.StringVar(value='0')
        self.mm = tk.StringVar(value='0')
        self.ss = tk.StringVar(value='0')
        self.lat_now = tk.StringVar(value='0')
        self.lon_now = tk.StringVar(value='0')
        #hh.set('')
        #hh.get()
        self.distance_to_goal = tk.StringVar(value='0')
        self.direction_to_goal = tk.StringVar(value='0')

        self.show_text()

    def show_text(self):
        l0_0 = tk.Label(self, text='ゴールの座標',font=("MSゴシック", "10"))

        text_goal_position = self.read_goal_position()
        l0_1 = tk.Label(self, text=text_goal_position,font=("MSゴシック", "20"))

        l0_2 = tk.Label(self, text=f'現在時刻：{self.hh.get()}時{self.mm.get()}分{self.ss.get()}秒',font=("MSゴシック", "12"))
        #l0_2 = tk.Label(self, text=f'現在時刻：{self.hh.get()}時{self.mm.get()}分{self.ss.get()}秒',font=("MSゴシック", "12"))
        #l0_2 = tk.Label(self, textvariable=f'秒：{self.ss}',font=("MSゴシック", "12"))

        l0_3 = tk.Label(self, text='現在の座標',font=("MSゴシック", "10"))
        l0_4 = tk.Label(self, text=f'{self.lat_now.get()},{self.lon_now.get()}',font=("MSゴシック", "20"))
        
        l0_5 = tk.Label(self, text='現在位置からゴールまで',font=("MSゴシック", "15"))
        l0_6 = tk.Label(self, text=f'距離：{self.distance_to_goal.get()}[km],方位{self.direction_to_goal.get()}[deg]',font=("MSゴシック", "30"))

        b0_0 = tk.Button(self, text="update start", fg="blue",command=self.get_position)

        #終了ボタン
        quit = tk.Button(self, text="stop update", fg="red",command=self.stop_update)

        i=0
        for e in [l0_2,l0_0,l0_1,quit,b0_0,l0_3,l0_4,l0_5,l0_6]:
            i = i + 1
            #e.pack(side='top', padx=5)
            e.grid(row=i,padx=5)
    
    def stop_update(self):
        #self.master.destroy
        self.after_cancel(self.after_id)
        print('end')

    def read_goal_position(self):
        self.path = os.getcwd()
        file_path = self.path + '\goal_position.csv'
        with open(file_path) as f:
            text_goal_position = f.read()
        self.goal_position = text_goal_position.split(',')
        return text_goal_position

    def get_position(self):
        ser = serial.Serial("COM3",9600,timeout=10)
        buff_NMEA = ser.readline()
        buff_NMEA_decode = buff_NMEA.decode()
        buff = buff_NMEA_decode.split(',')
        while(not buff[0] == '$GPRMC'):
            buff_NMEA = ser.readline()
            buff_NMEA_decode = buff_NMEA.decode()
            buff = buff_NMEA_decode.split(',')
        ser.close()

        world_time = buff[1]
        status = buff[2]
        latitude_dms = buff[3]
        longitude_dms = buff[5]

        JST = self.toJST(world_time)
        self.hh.set(JST[0])
        self.mm.set(JST[1])
        self.ss.set(JST[2])
        
        if(status == 'A'):
            position = self.toDD(latitude_dms,longitude_dms)
            self.lat_now.set(position[0])
            self.lon_now.set(position[1])
            dist = self.cal_dist(6378.137,self.goal_position[0],self.goal_position[1],self.lat_now.get(),self.lon_now.get())
            self.distance_to_goal.set(dist[0])
            self.direction_to_goal.set(dist[1])
        else:
            self.lat_now.set('0')
            self.lon_now.set('0')
            self.distance_to_goal.set('0')
            self.direction_to_goal.set('0')
        
        self.show_text()
        self.save_data()
        #self.get_position()
        self.after_id = self.after(500, self.get_position)

    def toJST(self,time):
        hh_int = int(time[0:2])
        if(hh_int + 9 >= 24):
            hh_int = hh_int + 9 - 24
        else:
            hh_int = hh_int + 9
        if(hh_int<10):
            hh = '0' + str(hh_int)
        else:
            hh = str(hh_int)
        mm = time[2:4]
        ss = time[4:6]
        return [hh,mm,ss]

    def toDD(self,latitude_dms,longitude_dms):
        latitude_dms_float = float(latitude_dms) / 100.0
        latitude_d = int(latitude_dms_float) + (latitude_dms_float - int(latitude_dms_float))*100.0/60.0
        longitude_dms_float = float(longitude_dms) / 100.0
        longitude_d = int(longitude_dms_float) + (longitude_dms_float - int(longitude_dms_float))*100.0/60.0
        position = [f'{latitude_d:.6f}',f'{longitude_d:.6f}']
        print(position)
        return position

    def cal_dist(self,_radius,_goal_lat, _goal_lon, _now_lat, _now_lon):
        goal_lat = math.radians(float(_goal_lat))
        goal_lon = math.radians(float(_goal_lon))
        now_lat = math.radians(float(_now_lat))
        now_lon = math.radians(float(_now_lon))
        radius = float(_radius)
        delta_lon = goal_lon - now_lon
        dist = radius * math.acos(math.sin(goal_lat)*math.sin(now_lat) + math.cos(goal_lat)*math.cos(now_lat)*math.cos(delta_lon))
        azi = (180.0/3.1415926535)*math.atan2(math.sin(delta_lon), math.cos(now_lat)*math.tan(goal_lat) - math.sin(now_lat)*math.cos(delta_lon))
        if(azi < 0):
            azi = azi + 360.0
        print(f'{goal_lat},{goal_lon}:{now_lat},{now_lon}')
        print(f'{dist},{azi}')
        return [f'{dist:.4f}',f'{azi:.1f}']

    def save_data(self):
        file_path = self.path + '\log.csv'
        with open(file_path, 'a',newline="") as f:
            csv.writer(f).writerow([self.hh.get(),self.mm.get(),self.ss.get(),
            self.lat_now.get(),self.lon_now.get(),self.distance_to_goal.get(),self.direction_to_goal.get()])
        f.close()


root = tk.Tk()
root.title('test')
root.geometry('720x480')

app = position_Info(master=root)
frame1 = tk.Frame(root,width=360,height=240,borderwidth=4,relief='groove')
frame2 = tk.Frame(root,width=360,height=240,borderwidth=4,relief='groove')

#frame1.grid(row=0,column=1)
#frame2.grid(row=1,column=1)

#app.get_position()
root.mainloop()