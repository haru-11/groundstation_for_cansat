import tkinter as tk
import os
import csv

class Input_info(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,
            width=720,height=480,
            borderwidth=4,relief='groove')
        self.master = master
        #self.grid(row=0,column=0)
        self.pack()
        #self.pack_propagate(0)
        self.input_goal_position()
        #self.now_time()

    def input_goal_position(self):
        label1 = tk.Label(self, text='ゴールの座標を入力してください')
        label1.grid(row=0,column=0,columnspan=2)

        #値入力(lat)
        tk.Label(self, text='latitude:').grid(row=1,column=0)
        #label_lat.pack()
        self.goal_lat_box = tk.Entry(self)
        self.goal_lat_box['width'] = 20
        self.goal_lat_box.grid(row=1,column=1)
        #self.lat_box.pack()

        #値入力(lon)
        tk.Label(self, text='longtitude:').grid(row=2,column=0)
        #label_lat.pack()
        self.goal_lon_box = tk.Entry(self)
        self.goal_lon_box['width'] = 20
        self.goal_lon_box.grid(row=2,column=1)
        #self.lat_box.pack()

        #値実行 
        submit_btn = tk.Button(self,text='入力')
        submit_btn['command'] = self.input_mynow_position
        #submit_btn.pack(ipadx=20,ipady=10)
        submit_btn.grid(row=3,column=0,columnspan=2)

        self.view_goal_position()
        #self.now_time()

    #表示
    def view_goal_position(self):
        path = os.getcwd()
        self.file_path = path + '\goal_position.csv'
        with open(self.file_path) as f:
            text_goal_position = 'ゴールのlat,lon: ' + f.read()
        tk.Label(self,text=text_goal_position).grid(row=4,column=0)
        #self.message = tk.Label(self)
        #self.message.pack()
        #self.message.grid(row=4,column=1)

        #終了ボタン
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        #self.quit.pack(side="bottom")
        self.quit.grid(row=6,column=0,columnspan=2)
    
    def now_time(self):
        _JST = myGPS.JST
        tk.Label(self,text=f'現在時刻は：{_JST[0]}時{_JST[1]}分{_JST[2]}秒').grid(row=5,column=0,columnspan=2)

    def input_mynow_position(self):
        self.goal_position_lat = self.goal_lat_box.get()
        self.goal_position_lon = self.goal_lon_box.get()
        #self.message['text'] = self.goal_position_lat + ',' + self.goal_position_lon
        self.save_goal_position()
    
    def save_goal_position(self):
        with open(self.file_path, 'w') as f:
            csv.writer(f).writerow([self.goal_position_lat,self.goal_position_lon])
        self.view_goal_position()

root = tk.Tk()
root.title('test')
root.geometry('720x480')
app = Input_info(master=root)
#thread1 = th.Thread(target=myGPS.show_GPRMC(myGPS))
#thread2 = th.Thread(target=app.mainloop())

#thread1.start()
app.mainloop()
#mygps = serial_test.myGPS()
#thread2.start()