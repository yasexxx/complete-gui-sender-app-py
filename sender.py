import datetime
import json
import os
import socket
import threading
import time
import tkinter as tk
import wave
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Combobox, Entry, Progressbar
import tkinter.font as tkFont

import pyaudio
import scipy.io.wavfile as wav
from PIL import Image, ImageTk
import selectors
import struct


logo_png = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-select.ico'
pausing = False

class MainWindow(object):
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")
        self.master.title("Electors WiFi Sender")
        self.master.iconbitmap(r'{}'.format(logo_png))
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.frame.configure(background="orange")
        self.frame1 = tk.Frame(self.frame)
        self.frame1.configure(background= "orange")
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", height=500, width=500)
        self.mbutton = MainButton(self.frame1)
        self.frames = {}
        

        b0 = tk.Button(self.frame1, text="Setting", command=self.setting_window, fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')
        self.b1 = tk.Button(self.frame1, text='Emergency Alarm', command=self.emergency_window, fg='black',
                       bg='white', relief='solid',
                       width=25, font=('arial', 19, 'bold'))
        self.b2 = tk.Button(self.frame1, text='Hourly Bell', command=self.hourlybell_window, fg='black',
                       bg='white', relief='solid',
                       width=25,
                       font=('arial', 19, 'bold'))
        b3 = tk.Button(self.frame1, text="Exit", command=self.quiting, fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')

        self.b4 = tk.Button(self.frame1, text='Live Anouncement', command=self.live_window, fg='black', bg='white', relief='solid',
                       width=25, font=('arial', 19, 'bold'))
        self.b5 = tk.Button(self.frame1, text='Refresh', command=self.refresh_window, fg='black', bg='white', relief='solid',
                       width=10, font=('arial', 12, 'bold'))
        L1 = tk.Label(self.frame1, text="WiFi Sender", font=('arial', 15, 'bold'), bg='orange')
        L1.place(relx=.5, rely=0.06, anchor="center")
    

        b0.place(x=0, y=0)

        b3.place(x=2, relx=0.88, rely=0)
        self.b1.place(relx=0.5, rely=0.2, anchor='center')
        self.b2.place(relx=0.5, rely=0.4, anchor='center')
        self.b4.place(relx=0.5, rely=0.6, anchor='center')
        self.b5.place(relx=0.5, rely=0.9, anchor='center')

        today = str(datetime.date.today())
        self.clock = tk.Label(self.frame1, font=('arial', 10, 'bold'), fg='black', bg='white', width=12)
        self.date = tk.Label(self.frame1, text=today, font=('arial', 10, 'bold'), fg='black', bg='white', width=12)
        self.clock.place(relx=0.75, rely=0.8, anchor='center')
        self.date.place(relx=0.25, rely=0.8, anchor='center')
        
        self.b1['state'] = 'disabled'
        self.b2['state'] = 'disabled'
        self.b4['state'] = 'disabled'
        self.show_clk()
        self.gone_ = False

    def refresh_window(self):
        self.x = bool1.get()
        self.y = bool2.get()
        self.z = bool3.get()
        if self.x or self.y or self.z:
            self.b1['state'] = 'normal'
            self.b2['state'] = 'normal'
            self.b4['state'] = 'normal'
        else:
            self.b1['state'] = 'disabled'
            self.b2['state'] = 'disabled'
            self.b4['state'] = 'disabled'

    def quiting(self):
        self.master.destroy()


    def hide(self):
        self.master.withdraw()

    def setting_window(self):
        if not self.gone_:
            self.hide()
            self.page1 = PageOne(self)
            w = self.page1.prove()
            self.gone_ = w
        else:
            if self.page1 != None:
                w = self.page1.show()
                self.gone_ = w
                if w == False:
                    self.setting_window()
        


    def emergency_window(self):
        self.hide()
        PageTwo(self)


    def hourlybell_window(self):
        self.hide()
        PageThree(self)

    def live_window(self):
        self.hide()
        PageFour(self)

    def show(self):
        #self.master.state("zoomed")
        self.master.update()
        self.master.deiconify()

    def show_clk(self):
        timenow = time.strftime('%H:%M:%S %p')
        self.clock['text'] = timenow
        #self.clock.config(text=timer)
        self.clock.after(1000, self.show_clk)


class MainButton(object):
    def __init__(self, master):
        self.master = master
        self.f = 'name.txt';
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # t1 = threading.Thread(target=self._runn)
        # t1.start()

    def _runn(self):
        while True:

            self.ip = None
            self.port = None
            self.addr = (self.ip, self.port)
            try:
                self.sock.connect(self.addr)
            except Exception as e:
                print(e)
                time.sleep(2)

                continue
            else:
                break

    def error1(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Action is undone! \nSelect a file first")

    def exit1(self):
        exit()

    def stop(self):
        global pausing
        pausing = True
        MESSAGE1 = 'stop'
        self.sock.send(bytes(MESSAGE1, 'ascii'))
        time.sleep(0.1)

    def alarm(self):
        if not os.path.exists(self.f):
            self.error1()
        else:
            global pausing
            pausing = True
            MESSAGE2 = 'alarm'
            self.sock.send(bytes(MESSAGE2, 'ascii'))
            time.sleep(0.1)

    def live(self):
        MESSAGE3 = 'live'
        self.sock.send(bytes(MESSAGE3, 'ascii'))
        time.sleep(2)
        ip = None
        port = None
        Live_Client(ip, port)


#Settings
class PageOne(tk.Toplevel):
    def __init__(self, master):
        self.master1 = master
        tk.Toplevel.__init__(self)
        self.geometry("500x500")
        self.title("Settings")
        #self.state("zoomed")
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.frame.configure(background="white")
        self.frame1 = tk.Frame(self.frame)
        self.frame1.configure(background="orange")
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", height=500, width=500)

        L1 = tk.Label(self.frame1, text="Speaker 1: ", font=('arial', 15, 'bold'), bg="orange")
        L2 = tk.Label(self.frame1, text="Speaker 2: ", font=('arial', 15, 'bold'), bg='orange')
        L3 = tk.Label(self.frame1, text="SETTINGS", font=('arial', 15, 'bold'), bg='orange')
        L4 = tk.Label(self.frame1, text="Option to Connect:   -S1 (Speaker 1)   -S2 (Speaker 2)", font=('arial', 10, 'bold'),
                      bg='orange')
        L5 = tk.Label(self.frame1, text=":", font=('arial', 15, 'bold'), bg='orange')
        L6 = tk.Label(self.frame1, text=":", font=('arial', 15, 'bold'), bg='orange')
        L7 = tk.Label(self.frame1, text="IP Address", font=('arial', 12, 'bold'), bg='orange')
        L8 = tk.Label(self.frame1, text="Port", font=('arial', 12, 'bold'), bg='orange')
        self.set_button1 = tk.Button(self.frame1, text='Set', command=self.toggle_button_1, fg='black',
                                relief = 'raised',bg='white', width=6, height=1, font=('arial', 10, 'bold'))
        self.set_button2 = tk.Button(self.frame1, text='Set', command=self.toggle_button_2, fg='black',
                                relief = 'raised', bg='white', width=6, height=1, font=('arial', 10, 'bold'))

        set_button4 = tk.Button(self.frame1, text='Back', command=self.backOpt, fg='black',
                                bg='white', relief='solid', width=6, height=1, font=('arial', 10, 'bold'))
        E1 = Entry(self.frame1, font=('arial', 15, 'bold'), textvariable=ip_input, width=14)
        E2 = tk.Entry(self.frame1, font=('arial', 15, 'bold'), textvariable=ip_input_1, width=14)
        E1_1 = tk.Entry(self.frame1, font=('arial', 15, 'bold'), textvariable=port_input, width=5)
        E1_2 = tk.Entry(self.frame1, font=('arial', 15, 'bold'), textvariable=port_input_1, width=5)
        
        self.switch_variable = tk.StringVar()
        self.both_button = tk.Radiobutton(self.frame1, text="BOTH", variable=self.switch_variable,
                            command=self.selected_serv,indicatoron=False, value="both", width=8, font=('arial', 10, 'bold'))
        self.s1_button = tk.Radiobutton(self.frame1, text="S1 Only", variable=self.switch_variable,
                            command=self.selected_serv,indicatoron=False, value="s1", width=8,font=('arial', 10, 'bold'))
        self.s2_button = tk.Radiobutton(self.frame1, text="S2 Only", variable=self.switch_variable,
                            command=self.selected_serv, indicatoron=False, value="s2", width=8,font=('arial', 10, 'bold'))
        
        
        path1 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-final.png'
        path2 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\elector_logo.gif'
        path3 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\setting_logo.gif'
        load_img = Image.open(path1)
        load_img2 = Image.open(path2)
        load_img3 = Image.open(path3)
        wd = 70
        ht = 70
        wd1 = 80
        ht1 = 80
        img_res2 = load_img2.resize((wd, ht), Image.ANTIALIAS)
        img_res1 = load_img.resize((wd1, ht1), Image.ANTIALIAS)
        img_res3 = load_img3.resize((wd, ht), Image.ANTIALIAS)
        get_img = ImageTk.PhotoImage(img_res1)
        img_logo = tk.Label(self.frame1, image=get_img, bg="orange")
        get_img2 = ImageTk.PhotoImage(img_res2)
        img_logo2 = tk.Label(self.frame1, image=get_img2, bg="orange")
        get_img3 = ImageTk.PhotoImage(img_res3)
        img_logo3 = tk.Label(self.frame1, image=get_img3, bg='orange')

        img_logo.image = get_img
        img_logo2.image = get_img2
        img_logo3.image = get_img3

        img_logo.place(relx=0.1, rely=0.15, anchor="w")
        img_logo2.place(relx=0.73, rely=0.14, anchor="w")
        img_logo3.place(relx=0.42, rely=0.14, anchor="w")

        self.both_button.place(relx=.7, rely=.8, anchor="center")
        self.s1_button.place(relx=.3, rely=.8, anchor="center")
        self.s2_button.place(relx=.5, rely=.8, anchor="center")

        L1.place(relx=.15, rely=.3, anchor="center")
        L2.place(relx=.15, rely=.5, anchor="center")
        L3.place(relx=.5, rely=0.03, anchor="center")
        L4.place(relx=.04, rely=.70, anchor="w")
        L5.place(relx=.60, rely=.3, anchor="center")
        L6.place(relx=.60, rely=.5, anchor="center")
        L7.place(relx=.42, rely=.24, anchor="center")
        L8.place(relx=.67, rely=.24, anchor="center")
        self.set_button1.place(relx=.84, rely=.3, anchor="center")
        self.set_button2.place(relx=.84, rely=.5, anchor="center")
        #set_button3.place(relx=.7, rely=.8, anchor="center")
        set_button4.place(x=0, y=0)
        #set_button5.place(relx=.3, rely=.8, anchor="center")
        #set_button6.place(relx=.5, rely=.8, anchor="center")
        E1.place(relx=.42, rely=.3, anchor="center")
        E2.place(relx=.42, rely=.5, anchor="center")
        E1_1.place(relx=.68, rely=.3, anchor="center")
        E1_2.place(relx=.68, rely=.5, anchor="center")
        port_input.set(00000)
        port_input_1.set(00000)
        ip_input.set("")
        ip_input_1.set("")
        
        self.s1_on = False
        self.s2_on = False
        self.both_on = False
        self.s1_button['state'] = 'disabled'
        self.s2_button['state'] = 'disabled'
        self.both_button['state'] = 'disabled'

    def selected_serv(self):
        x = self.switch_variable.get()
        ip1 = ip_input.get()
        po1 = port_input.get()
        ip2 = ip_input_1.get()
        po2 = port_input_1.get()
        ip_t1 = 'IP Address 1: '+ip1
        po_t1 = 'Port Address 1: '+str(po1)
        ip_t2 = 'IP Address 2: '+ip2
        po_t2 = 'Port Address 2: '+str(po2)
        
        if (x == 's1'):
            bool1.set(True)
            bool2.set(False)
            bool3.set(False)
            _conn1.set(ip_t1)
            _conn2.set(po_t1)
            _conn3.set('IP Address 2: '+'Not available')
            _conn4.set('Port Address 2:'+'Not available')
            self.goto_connect()
        elif x == 's2':
            bool1.set(False)
            bool2.set(True)
            bool3.set(False)
            _conn1.set('Not available')
            _conn2.set('Port Address 2:'+'Not available')
            _conn3.set(ip_t2)
            _conn4.set(po_t2)
            self.goto_connect()
        elif x ==  'both':
            bool1.set(False)
            bool2.set(False)
            bool3.set(True)
            _conn1.set(ip_t1)
            _conn2.set(po_t1)
            _conn3.set(ip_t2)
            _conn4.set(po_t2)
            self.goto_connect()

        

    def toggle_button_1(self):
        i1 = ip_input.get()
        p1 = port_input.get()
        if (i1 is '') and (p1 is 0):
            print("Wrong")
        elif p1 is 0:
            print("wrong")
        elif i1 is '':
            print('WRong')
        else:
            if self.set_button1.config('relief')[-1] == 'sunken':
                self.set_button1.config(relief="raised")
                self.s1_on = False
                self.s1_button['state'] = 'disabled'
                self.both_button['state'] = 'disabled'
            else:
                self.set_button1.config(relief="sunken")
                self.s1_on = True
                if self.s2_on is True and self.s1_on is True:
                    self.both_button['state'] = 'normal'
                self.s1_button['state'] = 'normal'
                
                


    def toggle_button_2(self):
        i1 = ip_input_1.get()
        p1 = port_input_1.get()
        if (i1 is '') and (p1 is 0):
            print("Wrong")
        elif p1 is 0:
            print("wrong")
        elif i1 is '':
            print('WRong')
        else:
            if self.set_button2.config('relief')[-1] == 'sunken':
                self.set_button2.config(relief="raised")
                self.s2_on = False
                self.s2_button['state'] = 'disabled'
                self.both_button['state'] = 'disabled'
            else:
                self.set_button2.config(relief="sunken")
                self.s2_on = True
                if self.s2_on is True and self.s1_on is True:
                    self.both_button['state'] = 'normal'
                self.s2_button['state'] = 'normal'


    def show(self):
        try:
            self.deiconify()
            return True
        except:
            return False

    
    def prove(self):
        return True

    def backOpt(self):
        self.withdraw()
        self.master1.show()

    def goto_connect(self):
        self.withdraw()
        PageFive(self.master1)


    def save_ip(self):
        get_ip = open("Address.txt", "w+")
        __ip = ip_input.get()
        __port = port_input.get()
        ip_input.set(__ip)
        port_input.set(__port)

        if __ip is not None and __port is not None:
            add_addr = '{},{}'.format(__ip, __port)
            get_ip.write(add_addr)
            get_ip.close()

        else:
            print("Wrong ip")


#Emergency Alarm
class PageTwo(tk.Toplevel):
    def __init__(self, master):
        self.master2 = master
        tk.Toplevel.__init__(self)
        self.geometry("500x500")
        self.title("Emergency Bell")
        #self.state("zoomed")
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.frame.configure(background="white")
        self.frame1 = tk.Frame(self.frame)
        self.frame1.configure(background="orange")
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", height=500, width=500)
        self.f = "name.txt"
        self.str_1 = tk.StringVar()
        self.str_2 = tk.StringVar()
        self.str_3 = tk.StringVar()
        self.str_4 = tk.StringVar()
        self.done_sending_ = tk.StringVar()

        b1 = tk.Button(self.frame1, text="Browse", command=self.browse_button, fg='black', bg="white", relief='solid', width=11,
                       font=('arial', 11, 'bold'))
        self.b2 = tk.Button(self.frame1, text='Back', command=self.backOpt, fg='black',
                            bg='white', relief='solid', width=6, height=1, font=('arial', 10, 'bold'))
        self.b3 = tk.Button(self.frame1, text='Send', command=self.send_file, fg='black',
                            bg='white', relief='solid', width=15, height=1, font=('arial', 15, 'bold'))
        self.b4 = tk.Button(self.frame1, text='Stop', command=self.stop_send, fg='black',
                            bg='white', relief='solid', width=15, height=1, font=('arial', 15, 'bold'))
        self.b5 = tk.Button(self.frame1, text='Resume', command=self.resume_send, fg='black',
                            bg='white', relief='solid', width=15, height=1, font=('arial', 15, 'bold'))
        self.b6 = tk.Button(self.frame1, text='Pause', command=self.pause_send, fg='black',
                            bg='white', relief='solid', width=15, height=1, font=('arial', 15, 'bold'))
        b3 = tk.Button(self.frame1, text="Exit", command=self.closeOpt, fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')


        l1 = tk.Label(self.frame1, text="EMERGENCY BELL", font=('arial', 20, 'bold'), bg='orange')
        l2 = tk.Label(self.frame1, text="Name:", font=('arial', 12, 'bold'), bg='orange')
        l3 = tk.Label(self.frame1, text="Length:", font=('arial', 12, 'bold'), bg='orange')
        l4 = tk.Label(self.frame1, text="Size:", font=('arial', 12, 'bold'), bg='orange')
        l5 = tk.Label(self.frame1, text="Channels:", font=('arial', 12, 'bold'), bg='orange')
        l6 = tk.Label(self.frame1, text="Framerate:", font=('arial', 12, 'bold'), bg='orange')

        self.progressbar = Progressbar(self.frame1, orient="horizontal", length="350", mode="determinate",variable=progress_var)

        l7_ = tk.Label(self.frame1, text="", font=('arial', 12, 'bold'), bg='orange', textvariable=self.str_1)
        l8_ = tk.Label(self.frame1, text="", font=('arial', 12, 'bold'), bg='orange', textvariable=self.str_2)
        l9_ = tk.Label(self.frame1, text='', font=('arial', 12, 'bold'), bg='orange', textvariable=self.str_3)
        l10_ = tk.Label(self.frame1, text='', font=('arial', 12, 'bold'), bg='orange', textvariable=self.str_4)
        l11_ = tk.Label(self.frame1, text='0%', font=('arial', 12, 'bold'), bg='orange', textvariable=percentage_)
        # l13_ = Label(self, text='Done Sending!', font=('arial', 12, 'bold'), bg='orange', textvariable=None)
        l12_ = tk.Label(self.frame1, text='Sending. . .', font=('arial', 12, 'bold'), bg='orange',
                        textvariable=self.done_sending_)
        path1 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-final.png'
        path2 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\elector_logo.gif'
        path3 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\alarm.gif'
        load_img = Image.open(path1)
        load_img2 = Image.open(path2)
        load_img3 = Image.open(path3)
        wd = 70
        ht = 70
        wd1 = 80
        ht1 = 80
        img_res2 = load_img2.resize((wd,ht), Image.ANTIALIAS)
        img_res1 = load_img.resize((wd1, ht1), Image.ANTIALIAS)
        img_res3 = load_img3.resize((wd1, ht1), Image.ANTIALIAS)
        get_img = ImageTk.PhotoImage(img_res1)
        img_logo = tk.Label(self.frame1, image=get_img, bg="orange")
        get_img2 = ImageTk.PhotoImage(img_res2)
        img_logo2 = tk.Label(self.frame1, image=get_img2, bg="orange")
        get_img3 = ImageTk.PhotoImage(img_res3)
        img_logo3 = tk.Label(self.frame1, image=get_img3, bg="orange")


        img_logo.image = get_img
        img_logo.place(relx=0.08, rely=0.18, anchor="w")
        img_logo2.image = get_img2
        img_logo2.place(relx=0.73, rely=0.17, anchor="w")
        img_logo3.image = get_img3
        img_logo3.place(relx=0.40, rely=0.17, anchor="w")

        b1.place(relx=0.66, rely=0.3, anchor="w")

        self.b2.place(x=0, y=0)
        self.b3.place(relx=0.08, rely=0.75, anchor="w")
        self.b4.place(relx=0.50, rely=0.75, anchor="w")
        self.b5.place(relx=0.08, rely=0.85, anchor="w")
        self.b6.place(relx=0.50, rely=0.85, anchor="w")
        b3.place(x=2, relx=0.88, rely=0)

        l1.place(relx=0.5, rely=0.05, anchor="center")
        l2.place(relx=0.08, rely=0.3, anchor="w")
        l3.place(relx=0.08, rely=0.4, anchor="w")
        l4.place(relx=0.08, rely=0.5, anchor="w")
        l5.place(relx=0.45, rely=0.4, anchor="w")
        l6.place(relx=0.45, rely=0.5, anchor="w")

        self.progressbar.place(relx=0.08, rely=0.6, anchor="w")

        l7_.place(relx=0.22, rely=0.4, anchor="w")
        l8_.place(relx=0.22, rely=0.5, anchor="w")
        l9_.place(relx=0.63, rely=0.4, anchor="w")
        l10_.place(relx=0.63, rely=0.5, anchor="w")
        l11_.place(relx=0.81, rely=0.6, anchor="w")
        # l13_.place(x=40, y=200)
        l12_.place(relx=0.08, rely=0.66, anchor="w")
        self.b4["state"] = "disabled"
        self.b5["state"] = "disabled"
        self.b6["state"] = "disabled"
        percentage_.set("0%")

        self.sound_list = {}
        _songlist = "songlist.txt"
        if os.path.exists(_songlist):
            sound = open(_songlist, "r+")
            js_song = sound.read()
            values = json.loads(js_song)
            if values is not None:
                self.sound_list = {**self.sound_list, **values}
                values = list(self.sound_list.keys())

            else:
                values = ''
        else:
            values = ''

        self.combo = Combobox(self.frame1, height="10", width="30", values=values)
        self.combo.place(relx=0.22, rely=0.3, anchor="w")
        self.combo.bind("<<ComboboxSelected>>", self.on_select)
        if values is not '' and values is not None:
            self.combo.current(0)

        self.stop1 = False
        self.pause2 = False

        self.resume1 = False
        self.done__ = False


        self.chunks = 1000

        # self.ip = '127.0.0.1'
        # self.port = 12345
        self.ip = ip_input.get()
        self.port = port_input.get()
        self.client2 = Client2_Send(ip=self.ip, port=self.port)


    def on_select(self, event=None):
        x = event.widget.get()
        print(x)
        locs = self.sound_list[x]
        self.change_text(locs)
        fw = open(self.f, "w+")
        fw.write(locs)
        fw.close()

    def closeOpt(self):
        self.master2.quiting()

    def backOpt(self):
        self.destroy()
        self.master2.show()

    def sending_frame(self):
        def _send_label():
            self.done__ = False
            while True:
                if self.done__:
                    break
                self.done_sending_.set("Sending")
                time.sleep(1)
                if self.done__:
                    break
                self.done_sending_.set("Sending.")
                time.sleep(1)
                if self.done__:
                    break
                self.done_sending_.set("Sending. .")
                time.sleep(1)
                if self.done__:
                    break
                self.done_sending_.set("Sending. . .")
                time.sleep(1)
                if self.done__:
                    break

        t1 = threading.Thread(target=_send_label, daemon=True)
        t1.start()

    def send_file(self):
        def __progress():
            file = open('name.txt', 'r+')
            file = file.read()
            wf = wave.open(file, 'rb')
            size = wf.getnframes()
            num_packets = int((size/self.chunks)+1)
            self.resume1 = False
            self.stop1 = False
            self.pause2 = False
            self.b2["state"] = "disabled"
            self.b3["state"] = "disabled"
            self.b4["state"] = "normal"
            self.b5["state"] = "disabled"
            self.b6["state"] = "normal"
            # total = 1023450
            # sps = 4098
            self.progressbar['maximum'] = num_packets
            self.sending_frame()
            ###----
            self.client2.running_all()
            ###----
            self.done__ = True
            time.sleep(1)
            self.done_sending_.set("Done sending!")
            percentage_.set("0%")
            self.progressbar.stop()
            progress_var.set(0)
            self.b2["state"] = "normal"
            self.b3["state"] = "normal"
            self.b4["state"] = "disabled"
            self.b5["state"] = "disabled"
            self.b6["state"] = "disabled"
            time.sleep(1)
            self.done_sending_.set("Select a sound to send")

        t1 = threading.Thread(target=__progress, daemon=True)
        t1.start()

    def resume_send(self):
        self.done__ = False
        self.resume1 = True
        self.client2.waveclient.resume_play()
        self.b5["state"] = "disabled"
        self.b6["state"] = "normal"

    def stop_send(self):
        def stop_send_():
            self.stop1 = True
            self.done__ = True
            self.client2.waveclient.stop_play()
            time.sleep(1)
            self.done_sending_.set("Select a sound to send.")
            percentage_.set("0%")
            self.progressbar.stop()
            self.b2["state"] = "normal"
            self.b3["state"] = "normal"
            self.b4["state"] = "disabled"
            self.b5["state"] = "disabled"
            self.b6["state"] = "disabled"

        t1 = threading.Thread(target=stop_send_, daemon=True)
        t1.start()

    def pause_send(self):
        def pause_send_():
            self.client2.waveclient.pause_play()
            self.pause2 = True
            self.done__ = True
            self.b5["state"] = "normal"
            self.b6["state"] = "disabled"
            time.sleep(1)
            self.done_sending_.set("Sending is paused.")

        t1 = threading.Thread(target=pause_send_, daemon=True)
        t1.start()

    def browse_button(self):
        def browse_button_():
            filename1 = filedialog.askopenfilename(initialdir="/", title="Choose a file",
                                                   filetypes=(("Sound files", ".wav"), ("All files", "*.*")))
            name1 = os.path.basename(filename1)
            add_name_1 = filename1  # f"Filename: {name1} \nPath: {filename1}"
            fw = open(self.f, "w+")
            fw.write(add_name_1)
            fw.close()
            if filename1 is not '' and name1 is not '':
                if name1 not in self.sound_list:
                    self.sound_list[name1] = filename1
                self.combo.set(name1)
                self.combo['values'] = list(self.sound_list.keys())
                self.combo.current()
                save_song = open("songlist.txt", "w+")
                str_js = json.dumps(self.sound_list)
                save_song.write(str_js)
                save_song.close()
                self.change_text(filename1)

        t1 = threading.Thread(target=browse_button_, daemon=True)
        t1.start()

    def change_text(self, filename1):
        def change_text_(filename1):
            wf = wave.open(filename1, 'rb')
            size = os.path.getsize(filename1)
            (source_rate, source_sig) = wav.read(filename1)
            duration_seconds = len(source_sig) / float(source_rate)
            size = size / 1000
            size1 = size / 1000
            size1 = round(size1, 1)
            size = int(size)
            if len(str(size)) >= 6:
                size = ''.join(str(size1) + " MB")
            else:
                size = ''.join(str(size) + " KB")
            chn = wf.getnchannels()
            fr = wf.getframerate()
            fr = ''.join(str(fr) + " Hz")
            duration_seconds = "".join(str(int(duration_seconds)) + " sec")
            if duration_seconds and size and chn and fr:
                self.str_1.set(duration_seconds)
                self.str_2.set(size)
                self.str_3.set(chn)
                self.str_4.set(fr)

        t1 = threading.Thread(target=change_text_, args=(filename1,), daemon=True)
        t1.start()


#Hourly Bell
class PageThree(tk.Toplevel):
    def __init__(self, master):
        self.master2 = master
        tk.Toplevel.__init__(self)
        self.geometry("500x500")
        self.title("Emergency Bell")
        #self.state("zoomed")
        self.start_var = tk.StringVar(value = '')
        self.end_var = tk.StringVar(value = '')
        self.interval_var = tk.IntVar(value=0)
        self.song_var = tk.StringVar()
        self.song_invalid = False
        vcmd = (self.register(self.onValidate), '%d', '%s', '%S')

        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.frame.configure(background="white")
        self.frame1 = tk.Frame(self.frame)
        self.frame1.configure(background="orange")
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", height=500, width=500)
        Lh0 = tk.Label(self.frame1, text='HOURLY BELL', font=('arial', 20, 'bold'), bg='orange')
        Lh1 = tk.Label(self.frame1, text='Time Start:', font=('arial', 20, 'bold'), bg='orange')
        Lh2 = tk.Label(self.frame1, text='Time End :', font=('arial', 20, 'bold'), bg='orange')
        Lh3 = tk.Label(self.frame1, text='Interval:', font=('arial', 20, 'bold'), bg='orange')
        Lh4 = tk.Label(self.frame1, text='Operation Logs:', font=('arial', 12, 'bold'), bg='orange')
        Lh5 = tk.Label(self.frame1, text='- in minutes', font=('arial', 8, 'bold'), bg='orange')
        self.Eh1 = tk.Entry(self.frame1, width=14, font=('arial', 12, 'bold'), validate='key', validatecommand= vcmd,bd=5, justify = 'center', textvariable =self.start_var)
        self.Eh2 = tk.Entry(self.frame1, width=14, font=('arial', 12, 'bold'), validate='key', validatecommand= vcmd, bd=5, justify = 'center', textvariable =self.end_var)
        self.Eh3 = tk.Entry(self.frame1, width=14, font=('arial', 12, 'bold') ,bd=5, justify = 'center', textvariable =self.interval_var)

        hbbrowse = tk.Button(self.frame1, text="Browse", command=self.browse_button, fg='black', bg="white", relief='solid', width=10,
                             font=('arial', 12, 'bold'), height=2)

        set_button2 = tk.Button(self.frame1, text='Set', command=self.set_button, fg='black',
                                bg='white', relief='solid', width=10, height=2,
                                font=('arial', 12, 'bold'))
        self.b1 = tk.Button(self.frame1, text='Back', command=self.backOpt, fg='black',
                            bg='white', relief='solid', width=6, height=1, font=('arial', 10, 'bold'))
        
        self.b2 = tk.Button(self.frame1, text='Delete\nLog', command=self.delete, fg='black',
                            bg='white', relief='solid', width=5, font=('arial', 8, 'bold'))

        self.clock = tk.Label(self.frame1, font=('arial', 10, 'bold'), fg='black', bg='white', width=12)

        path1 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-final.png'
        path2 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\elector_logo.gif'
        path3 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\bell.gif'
        load_img = Image.open(path1)
        load_img2 = Image.open(path2)
        load_img3 = Image.open(path3)
        wd = 70
        ht = 70
        wd1 = 80
        ht1 = 80
        img_res2 = load_img2.resize((wd, ht), Image.ANTIALIAS)
        img_res1 = load_img.resize((wd1, ht1), Image.ANTIALIAS)
        img_res3 = load_img3.resize((wd, ht), Image.ANTIALIAS)
        get_img = ImageTk.PhotoImage(img_res1)
        img_logo = tk.Label(self.frame1, image=get_img, bg="orange")
        get_img2 = ImageTk.PhotoImage(img_res2)
        img_logo2 = tk.Label(self.frame1, image=get_img2, bg="orange")
        get_img3 = ImageTk.PhotoImage(img_res3)
        img_logo3 = tk.Label(self.frame1, image=get_img3, bg='orange')

        img_logo.image = get_img
        img_logo2.image = get_img2
        img_logo3.image = get_img3
        
        Lh0.place(x=160, y=10)
        Lh1.place(relx=0.20, rely=0.35, anchor='w')
        Lh2.place(relx=0.20, rely=0.45, anchor='w')
        Lh3.place(relx=0.20, rely=0.55, anchor='w')
        Lh4.place(relx=0.05, rely=0.75, anchor='w')
        Lh5.place(relx=0.20, rely=0.59, anchor='w')
        self.Eh1.place(relx=0.55, rely=0.35, anchor='w')
        self.Eh2.place(relx=0.55, rely=0.45, anchor='w')
        self.Eh3.place(relx=0.55, rely=0.55, anchor='w')
        hbbrowse.place(relx=0.25, rely=0.67, anchor='w')
        set_button2.place(relx=0.55, rely=0.67, anchor='w')

        img_logo.place(relx=0.1, rely=0.18, anchor="w")
        img_logo2.place(relx=0.73, rely=0.17, anchor="w")
        img_logo3.place(relx=0.42, rely=0.17, anchor="w")
        self.b1.place(x=0, y=0)
        self.b2.place(relx=0.86, rely=0.85, anchor="w")
        
        self.clock.place(relx=0.5, rely=0.26, anchor='n')
    
        self.car_header = [' Filename ', ' Time Start ', ' Time End ', ' Interval(-min.) ',' Active ']
        self.car_list = []
        self.pick_sound = {}
        if os.path.exists('sound.txt'):
            read_sound = open('sound.txt', 'r+')
            file0 = read_sound.read()
            file0 = json.loads(file0)
        else:
            file0 = {}
        self.pick_sound = {**self.pick_sound, **file0}
        self.del_logs = False

        self._setup_widgets()

        self.show_clk()
        ip = ip_input.get()
        port = port_input.get()
        #ip = '127.0.0.1'
        #port = 12345
        
        self.client3 = Client3_Send(ip=ip, port=port)
        self.Eh1.bind('<KeyRelease>', self.timemask)
        self.Eh2.bind('<KeyRelease>', self.timemask)

        

    def onValidate(self, d, s, S):
        if d == "0":
            return True
        # Allow only digit, ":" and check the length of the string
        if ((S == ":" and len(s) != 2 and len(s) != 5 ) or (not S.isdigit() and
                S != ":") or (len(s) == 3 and int(S) > 5) or (len(s) == 6 and int(S) > 5) or len(s) > 7):
            self.bell()
            return False
        return True

    def timemask(self, event):
        s = event.widget
        # if delete a char do return ok or delete the char ":" and the previous number
        if len(s.get()) == 2 and event.keysym=="BackSpace":
            s.delete(len(s.get())-1, tk.END)
        if event.keysym=="BackSpace":
            return
        # check the hour format and add : between hours and minutes
        if len(s.get()) == 1 and int(s.get()) > 2:
            s.insert(0, "0")
            s.insert("end", ":")
        elif len(s.get()) == 2 and int(s.get()) < 24:
            s.insert(2, ":")
        elif len(s.get()) >= 2 and s.get()[2:3] != ":":
            self.bell()
            s.delete(1, tk.END)
        elif len(s.get()) == 5 and int(s.get()[3:5]) < 60:
            s.insert(5, ":")
        elif len(s.get()) >= 5 and s.get()[5:6] != ":":
            self.bell()
            s.delete(4, tk.END)


    def browse_button(self):
        def browse_button_():
            filename = filedialog.askopenfilename(initialdir="/", title="Choose a file",
                                                   filetypes=(("Sound files", ".wav"), ("All files", "*.*")))
            name = os.path.basename(filename)
            add_name_ = filename  # f"Filename: {name1} \nPath: {filename1}"
            fw = open('sound loc.txt', "w+")
            fw.write(add_name_)
            fw.close()
            item_source.set(add_name_)
            if filename is not '' and name is not '':
                if name not in self.pick_sound:
                    self.pick_sound[name] = filename
                save_sound = open('sound.txt', 'w+')
                str_sound = json.dumps(self.pick_sound)
                save_sound.write(str_sound)
                save_sound.close()
                self.song_var.set(name)

        t1 = threading.Thread(target=browse_button_, daemon=True)
        t1.start()

    def set_button(self):
        start_time = self.start_var.get()
        end_time = self.end_var.get()
        interval1 = self.interval_var.get()
        interval = int(interval1*60)
        active = 'Yes'
        song = self.song_var.get()
        if song is not None and song !='':
            self.song_invalid = False
        else: self.song_invalid = True
        if not self.song_invalid:
            if (start_time != '00:00:00') and (end_time != '00:00:00') and (interval != 0):
                song_load_1 = song
                if (len(start_time) == 8) and (len(end_time) == 8):
                    parts = start_time.split(':')
                    parts_2 = end_time.split(':')
                    s_time = int(parts[0])*(60*60) + int(parts[1])*60 + int(parts[2])
                    e_time = int(parts_2[0])*(60*60) + int(parts_2[1])*60 + int(parts_2[2])
                    ss = int(s_time)
                    ee = int(e_time)
                    ii = int(interval)
                    print(ss, ee, ii)
                    if (ss < ee) and (ss+ii<=ee): 
                        add = (song_load_1, start_time, end_time, interval1, active)
                        add_1 = (song_load_1, start_time, end_time, interval, active)
                        if add not in self.car_list:
                            jso_n = json.dumps(add_1)
                            self.start_timing(jso_n)
                            self.car_list.append(add)
                            self.tree.insert('', 'end', values=add)
                            for ix, val in enumerate(add):
                                col_w = tkFont.Font().measure(val)
                                if self.tree.column(self.car_header[ix],width=None)<col_w:
                                    self.tree.column(self.car_header[ix], width=col_w)


    def start_timing(self, package,):
        msg = json.loads(package)
        self.msg = msg
        audio = msg[0]
        st = msg[1]
        et = msg[2]
        int1 = msg[3]
        active_ = msg[4]
        if active_ == 'Yes':
            self.go_timing(st,et,int1,audio)


    def go_timing(self, st, et, ti, src):
        new_st = st.split(':')
        new_et = et.split(':')
        time_st = int(new_st[0])*(60*60) + int(new_st[1])*60 + int(new_st[2])
        time_et = int(new_et[0])*(60*60) + int(new_et[1])*60 + int(new_et[2])
        get_item = []
        for i in range(time_st, time_et, ti):
            get_item.append(i)
        last = get_item.pop()
        st = time.strftime('%H:%M:%S', time.gmtime(last))
        for i in range(time_st, time_et, ti):
            st = time.strftime('%H:%M:%S', time.gmtime(i))
            if i == last:
                t1 = threading.Thread(target=self.start_TIME_last, args=(st,et,src,), daemon=True)
                t1.start()
            else:
                t =threading.Thread(target=self.start_TIME, args=(st,src,), daemon=True)
                t.start()
   
    
    def start_TIME(self, time1, src):
        while True:
            if(time1 == time.strftime('%H:%M:%S')):
                self.client3.running_all(src)
                break
            time.sleep(0.5)

    def start_TIME_last(self, time1,t1, src):
        while True:
            if(time1 == time.strftime('%H:%M:%S')):
                self.client3.running_all(src)
                break
            time.sleep(0.5)
        x = self.tree.get_children()
        for i in x:
            val = self.tree.item(i)['values']
            if t1 in val:
                val.pop()
                add = 'No'
                val.append(add)
                self.tree.item(i, values=val)
        

    def show_clk(self):
        timenow = time.strftime('%H:%M:%S %p')
        self.clock['text'] = timenow
        #self.clock.config(text=timer)
        self.clock.after(1000, self.show_clk)

    def backOpt(self):
        self.destroy()
        self.master2.show()

    def _setup_widgets(self):
        container = ttk.Frame(self.frame1)
        container.place(relx=0.05, rely=0.88, anchor='w')
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(self.frame1,columns=self.car_header, show="headings", height=3)
        vsb = ttk.Scrollbar(container ,orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(container,orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        for col in self.car_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))
    
    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, \
            int(not descending)))

    def on_select(self, event=None):
        self.select = event.widget.selection()
        if self.select:
            self.del_logs = True

    def delete(self):
        if self.del_logs:
            if self.select != None and self.select !='':
                for i in self.select:
                    x = self.tree.item(i)['values']
                    self.tree.delete(i)
            self.del_logs = False

        

#Live Announcement
class PageFour(tk.Toplevel):
    def __init__(self, master):
        self.master2 = master
        tk.Toplevel.__init__(self)
        self.geometry("500x500")
        self.title("Emergency Bell")
        #self.state("zoomed")
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.frame.configure(background="white")
        self.frame1 = tk.Frame(self.frame)
        self.frame1.configure(background="orange")
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", height=500, width=500)
        b1 = tk.Button(self.frame1, text='Back', command=self.backOpt, fg='black',
                       bg='white', relief='solid', width=6, height=1,
                       font=('arial', 10, 'bold'))
        self.b2 = tk.Button(self.frame1,text='Play', command=lambda: self.record_time(0), fg='black',
                                bg='white', relief='solid', width=15, height=2,
                                font=('arial', 10, 'bold'))
    
        self.b3 = tk.Button(self.frame1,text='Stop', command=self.stop_button, fg='black',
                                bg='white', relief='solid', width=15, height=2,
                                font=('arial', 10, 'bold'))
        Lh0 = tk.Label(self.frame1, text='LIVE ANNOUNCEMENT', font=('arial', 20, 'bold'), bg='orange')
        Lh1 = tk.Label(self.frame1, text='Time Elapsed:', font=('arial', 20, 'bold'), bg='orange')
        self.Lh2 = tk.Label(self.frame1, text='00:00:00', font=('arial', 20, 'bold'), bg='orange')
        
        path1 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-final.png'
        path2 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\elector_logo.gif'
        path3 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\mic.gif'
        load_img = Image.open(path1)
        load_img2 = Image.open(path2)
        load_img3 = Image.open(path3)
        wd = 70
        ht = 70
        wd1 = 80
        ht1 = 80
        img_res2 = load_img2.resize((wd, ht), Image.ANTIALIAS)
        img_res1 = load_img.resize((wd1, ht1), Image.ANTIALIAS)
        img_res3 = load_img3 #load_img3.resize((wd, ht), Image.ANTIALIAS)
        get_img = ImageTk.PhotoImage(img_res1)
        img_logo = tk.Label(self.frame1, image=get_img, bg="orange")
        get_img2 = ImageTk.PhotoImage(img_res2)
        img_logo2 = tk.Label(self.frame1, image=get_img2, bg="orange")
        get_img3 = ImageTk.PhotoImage(img_res3)
        img_logo3 = tk.Label(self.frame1, image=get_img3, bg='orange')

        img_logo.image = get_img
        img_logo2.image = get_img2
        img_logo3.image = get_img3
        

        
        b1.place(x=0, y=0)
        self.b2.place(relx=.2, rely=0.6, anchor='w')
        self.b3.place(relx=.55, rely=0.6, anchor='w')
        Lh0.place(relx=0.50, rely=0.05, anchor='center')
        Lh1.place(relx=0.18, rely=0.40, anchor='w')
        self.Lh2.place(relx=0.58, rely=0.40, anchor='w')

        img_logo.place(relx=0.1, rely=0.18, anchor="w")
        img_logo2.place(relx=0.73, rely=0.17, anchor="w")
        img_logo3.place(relx=0.35, rely=0.18, anchor="w")


        
    def record_time(self,s):
        ip1 = ip_input.get()
        port1 = port_input.get()
        ip2 = ip_input_1.get()
        port2 = port_input_1.get()
        self.client = Client_Send(ip=ip1, port=port1, ip2=ip2, port2=port2)
        self.client.running_all()
        live_run.set(True)
        self.record_time2(s)


    def record_time2(self, s):
        timee = s
        if live_run.get():
            time_start = time.strftime('%H:%M:%S', time.gmtime(timee))
        else:
           time_start = time.strftime('%H:%M:%S', time.gmtime(0))
        self.b2['state'] ="disabled"
        self.Lh2['text'] = time_start
        self._job = self.after(1000,self.record_time2, s+1)
    
        
        
    def stop_button(self):
        self.client.live.stop_playing()
        time_start = time.strftime('%H:%M:%S', time.gmtime(0))
        self.Lh2['text'] = time_start
        self.cancel_()
        self.b2['state'] ="normal"

    def cancel_(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
    

    def backOpt(self):
        self.destroy()
        self.master2.show()


#Connect Page
class PageFive(tk.Toplevel):
    def __init__(self, master):
        self.master2 = master
        tk.Toplevel.__init__(self)
        self.geometry("500x500")
        self.title("Emergency Bell")
        #self.state("zoomed")
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.frame.configure(background="white")
        self.frame1 = tk.Frame(self.frame)
        self.frame1.configure(background="orange")
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", height=500, width=500)
        self.b1 = tk.Button(self.frame1, text='Home', command=self.exit_, fg='black',
                       bg='white', relief='solid', width=6, height=1,
                       font=('arial', 10, 'bold'))

        Lh0 = tk.Label(self.frame1, text='Wi-Fi Sender', font=('arial', 20, 'bold'), bg='orange')
        self.Lh1 = tk.Label(self.frame1, text='', font=('arial', 14, 'bold'), bg='orange', fg='maroon')
        self.Lh2 = tk.Label(self.frame1, text='IP Address 1: 192.168.254.115', textvariable=_conn1, font=('arial', 12, 'bold'), bg='orange')
        self.Lh3 = tk.Label(self.frame1, text='Port Address 1: 8080',  textvariable=_conn2,font=('arial', 12, 'bold'), bg='orange')
        self.Lh4 = tk.Label(self.frame1, text='IP Address 2: 192.168.254.115',  textvariable=_conn3, font=('arial', 12, 'bold'), bg='orange')
        self.Lh5 = tk.Label(self.frame1, text='Port Address 2: 8080',  textvariable=_conn4,font=('arial', 12, 'bold'), bg='orange')
        self.Lh6 = tk.Label(self.frame1, text='Status:', font=('arial', 12, 'bold'), bg='orange')
        self.Lh7 = tk.Label(self.frame1, text='Speaker 1: Connecting' , font=('arial', 12, 'bold'), bg='orange',)
        self.Lh8 = tk.Label(self.frame1, text='Speaker 2: Connecting', font=('arial', 12, 'bold'), bg='orange')
        path1 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-final.png'
        load_img = Image.open(path1)
        wd1 = 80
        ht1 = 80
        img_res1 = load_img.resize((wd1, ht1), Image.ANTIALIAS)
        get_img = ImageTk.PhotoImage(img_res1)
        img_logo = tk.Label(self.frame1, image=get_img, bg="orange")
        img_logo.image = get_img
        

        
        self.b1.place(x=0, y=0)
        Lh0.place(relx=0.50, rely=0.05, anchor='center')
        self.Lh1.place(relx=0.38, rely=0.32, anchor='w')
        self.Lh2.place(relx=0.3, rely=0.44, anchor='w')
        self.Lh3.place(relx=0.3, rely=0.49, anchor='w')
        self.Lh4.place(relx=0.3, rely=0.59, anchor='w')
        self.Lh5.place(relx=0.3, rely=0.64, anchor='w')
        self.Lh6.place(relx=0.3, rely=0.75, anchor='w')
        self.Lh7.place(relx=0.36, rely=0.80, anchor='w')
        self.Lh8.place(relx=0.36, rely=0.85, anchor='w')
        img_logo.place(relx=0.5, rely=0.10, anchor="n")

        self.not_yet_connect = True
        self.not_yet_connect_2 = True
        self.unsuccessful = False
        self.unsuccessful_2 = False
        self.connected_ = False
        self.connected_2 = False
        self.stop_1 = False
        self.text_connect_('.')

        ip1 = ip_input.get()
        po1 = port_input.get()
        ip2 = ip_input_1.get()
        po2 = port_input_1.get()
        self.address_1 =(ip1, po1)
        self.address_2 =(ip2, po2)
        
       
        t1 = threading.Thread(target=self.connect_1, daemon=True)
        t2 = threading.Thread(target=self.connect_2, daemon=True) 
        t1.start()
        t2.start()
        self.b1['state'] ='disabled'

    def text_connect_(self, s):
        txt = "Connecting"+s
        if len(txt)<20: 
            self.Lh1['text'] = txt
            self._job_1 = self.frame.after(1000, self.text_connect_, s+' .')
        else:
            if self._job_1 is not None:
                self.frame.after_cancel(self._job_1)
                self._job_1 = None
                if self.not_yet_connect and self.not_yet_connect_2:
                    self.text_connect_('.')
                else:
                    if self.unsuccessful and self.unsuccessful_2:
                        self.Lh1['text'] = 'Connection Failed'
                        self.b1['state'] ='normal'
                    else:
                        if bool1.get() == True:
                            if self.connected_:
                                self.cancel_d_job()
                                self.backOpt()
                                self.connected_ = False
                        elif bool2.get() == True:
                            if self.connected_2:
                                self.cancel_d_job()
                                self.backOpt()
                                self.connected_2 = False
                        elif bool3.get() == True:
                            if (self.connected_ and self.connected_2):
                                self.cancel_d_job()
                                self.backOpt()
                                self.connected_ = False
                                self.connected_2 = False
                        self.text_connect_('.')
                  

    def cancel_d_job(self):
        if self._job_1 is not None:
                self.frame.after_cancel(self._job_1)
                self._job_1 = None

    def exit_(self):
        self.destroy()
        self.master2.show()

    def backOpt(self):
        self.withdraw()
        self.master2.show()

    def connect_1(self):
        socket1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Connecting at",self.address_1 )
            socket1.connect(self.address_1)
            print("Connected!" )
        except Exception as e:
            print(e)
            self.connect_unsucessful_1()
            self.not_yet_connect = False
            self.unsuccessful =True
        else: self.connected_ = True

    def connect_2(self):
        socket1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Connecting at",self.address_2 )
            socket1.connect(self.address_2)
            print("Connected!" )
        except Exception as e:
            print(e)
            self.connect_unsucessful_2()
            self.not_yet_connect_2 = False
            self.unsuccessful_2 =True
        else: self.connected_2 = True

    def connect_unsucessful_1(self):
        t1 = 'Speaker 1: Connection Failed'
        self.Lh7['text'] = t1

    def connect_unsucessful_2(self):
        t1 = 'Speaker 2: Connection Failed'
        self.Lh8['text'] = t1

mysel = selectors.DefaultSelector()

class Client_Send(object):
    def __init__(self, ip=None, port=None, ip2=None, port2=None):
        super(Client_Send, self).__init__()

        self.success_connect_1 = True
        self.success_connect_2 = True

        if ip != None and port != None:
            self.ip = ip
            self.port = int(port)+1
            self.server_address = (self.ip, self.port)
        else:
            self.server_address = None
        if ip2 != None and port2 != None:
            self.ip2 = ip2
            self.port2 = int(port2)+1
            self.server_address_2 = (self.ip2, self.port2)
        else:
            self.server_address_2 = None
        self.keep_running = True

        json_ser1 = json.dumps(self.server_address)
        json_ser2 = json.dumps(self.server_address_2)
        self.live = Live_Client(json_ser1, json_ser2)

    def running_all(self):
        thread_1 = threading.Thread(target=self.server1_operate, daemon=True)
        thread_2 = threading.Thread(target=self.server2_operate, daemon=True)
        thread_1.start()
        thread_2.start()

        # self.server1_operate()
        # self.server2_operate()
        # self.server3_operate()

    def server1_operate(self):
        print('connecting to {} port {}'.format(*self.server_address))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.server_address)
        except Exception as e:
            print(f'error--1: {e}')
            self.success_connect_1 = False
            live_run.set(False)
        else:
            self.success_connect_1 = True
            print("Successfully connect to 1")
        if self.success_connect_1:
            sock.setblocking(False)

            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)
            # =========>
            # =========//////////
            self.main_operation()

    def server2_operate(self):
        print('connecting to {} port {}'.format(*self.server_address_2))
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock2.connect(self.server_address_2)
        except Exception as e:
            print(f'error--2: {e}')
            self.success_connect_2 = False
        else:
            self.success_connect_2 = True
        if self.success_connect_2:
            sock2.setblocking(False)
            print("Successfully connect to 2")
            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock2, selectors.EVENT_READ | selectors.EVENT_WRITE, data=self.service_bluff)
            # =========>
            # =========//////////
            self.main_operation_bluff()

    def main_operation(self):
        if self.keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                connection = key.fileobj
                self.client_address = connection.getpeername()
                print('client({})'.format(self.client_address))
                if mask & selectors.EVENT_WRITE:
                    self.service_operate(connection)

    def main_operation_bluff(self):
        if self.keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                callback = key.data
                callback(key.fileobj, mask)

    def service_bluff(self, key, mask):
        sock = key
        if mask & selectors.EVENT_WRITE:
            self.service_operate_bluff(sock)
        # print('shutting down')
        # mysel.unregister(connection)
        # connection.close()
        # mysel.close()

    def service_operate(self, conn):
        data = b'logarithmic'
        pack_data = struct.pack(">ii11s", 32, 2319, data)
        conn.sendall(pack_data)
        if pack_data:
            self.live.running_live()
            mysel.unregister(conn)
            conn.close()

    def service_operate_bluff(self, conn):
        data = b'logarithmic'
        pack_data = struct.pack(">ii11s", 32, 2319, data)
        conn.sendall(pack_data)
        if pack_data:
            print("done123")
            mysel.unregister(conn)
            conn.close()   



class Live_Client(object):
    def __init__(self, ip, ip2):
        super(Live_Client, self).__init__()
        ip_1 = ip
        ip_2 = ip2
        ip_1 = json.loads(ip_1)
        ip_2 = json.loads(ip_2)
        # self.ip = ip
        # self.port = port
        _ip1 = ip_1[0]
        _port1 = ip_1[1]+1
        _ip2 = ip_2[0]
        _port2 = ip_2[1]+1
        ip_3 = (_ip1, _port1)
        ip_4 = (_ip2, _port2)
        self.frames = []
        self.addresses = ip_3
        self.addresses_2 = ip_4
        self.pausing = False
        FORMAT = pyaudio.paInt16
        CHUNK = 1024
        self.chunk = CHUNK
        CHANNELS = 2
        RATE = 44100
        self.Audio = pyaudio.PyAudio()
        self.stream = self.Audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK,
                                      )


    def running_live(self):            
        self.AudioThread = threading.Thread(target=self.record, daemon=True)
        self.udpThread = threading.Thread(target=self.udpStream, daemon=True)
        self.AudioThread.start()
        self.udpThread.start()

    def udpStream(self):
        print("connecting live at ", self.addresses)
        print("were live now!")
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.z1 = udp
        while True:
            if self.pausing:
                break
            while True:
                if self.pausing:
                    break
                if len(self.frames) > 0:
                    frames_mod = self.frames.pop(0)
                    try:
                        self.z1.sendto(frames_mod, self.addresses)
                    except Exception as e:
                        #print(e)
                        pass
                    try:
                        self.z1.sendto(frames_mod, self.addresses_2)
                    except Exception as e:
                        pass
        print("closing socket")
        udp.close()

    def record(self):
        while True:
            if self.pausing:
                break
            self.frames.append(self.stream.read(self.chunk))
        print("closing recording")
        self.stream.stop_stream()
        self.stream.close()
        self.Audio.terminate()

    def stop_playing(self):
        self.pausing = True
        print("pausing")

    def resume_playing(self):
        self.pausing = False


class Client2_Send(object):
    def __init__(self, ip=None, port=None, ip2=None, port2=None):
        super(Client2_Send, self).__init__()

        self.success_connect_1 = True
        self.success_connect_2 = True
        self.keep_running = True
        
        if ip is not None and port is not None:
            self.ip = ip
            self.port = int(port)+1
            self.server_address = (self.ip, self.port)
        else:
            self.server_address = None
        if ip2 is not None and port2 is not None:
            self.ip2 = ip2
            self.port2 = int(port2)+1
            self.server_address_2 = (self.ip2, self.port2)
        else:
            self.server_address_2 = None

        self.waveclient = Client_wave()


    def running_all(self):
        file = open('name.txt', 'r+')
        source = file.read()
        self.source = source
        t1 = threading.Thread(target=self.server1_operate, daemon=True)
        t2 = threading.Thread(target=self.server2_operate, daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


    def server1_operate(self):
        print('connecting to {} port {}'.format(*self.server_address))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            sock.connect(self.server_address)
        except Exception as e:
            print(f'error--1: {e}')
            self.success_connect_1 = False
        else:
            self.success_connect_1 = True
            print("Successfully connect to 1")
        if self.success_connect_1:
            sock.setblocking(False)

            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, )
            # =========>
            # =========//////////
            self.main_operation()

    def server2_operate(self):
        try:
            print('connecting to {} port {}'.format(*self.server_address_2))
        except TypeError as e:
            pass
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock2.connect(self.server_address_2)
        except Exception as e:
            print(f'error--2: {e}')
            self.success_connect_2 = False
        else:
            self.success_connect_2 = True

        if self.success_connect_2:
            sock2.setblocking(False)
            print("Successfully connect to 2")
            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock2, selectors.EVENT_READ | selectors.EVENT_WRITE, )
            # =========>
            # =========//////////
            self.main_operation()


    def main_operation(self):
        if self.keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                connection = key.fileobj
                self.client_address = connection.getpeername()
                print('client({})'.format(self.client_address))
                if mask & selectors.EVENT_WRITE:
                    self.service_operate(connection)


    def service_operate(self, conn):
        data = b"xboxlive2020operate"
        pack_data = struct.pack(">i19si", 4020, data, 202304)
        conn.sendall(pack_data)
        if pack_data:
            address_1 = conn.getpeername()
            ip_add = address_1[0]
            port_add = address_1[1]
            source = self.source
            print("sending data")
            self.waveclient.operator_wav(ip_add,port_add, source)
            #w.operator_wav()
            mysel.unregister(conn)
            conn.close()



class Client_wave(object):
    def __init__(self):
        super(Client_wave, self).__init__()
        self.resume_play()
        self.done = False
        # if port is not None:
        #     self.port = int(port)
        self.frames = []
        #self.source = "waves.wav"   #####GENEL ari alisdi ang file pag send
        #self.destination = "_sample_wav.wav"

        self.chunks = 1000
        self.t = 0.00125
        self.Audio = pyaudio.PyAudio()
        self.connected_ = False
        
        self.stop1 = False
        self.pause2 = False
        self.resume1 = False
        self.done__ = False

    def operator_wav(self,ip, port, source):
        self.ip = ip
        self.port = port+1
        self.port_1 = port+2
        self.server_address = (self.ip, self.port)
        self.server_address_1 = (self.ip, self.port_1)
        self.source = source
        wf = wave.open(self.source, 'rb')
        sample_width = wf.getsampwidth()
        print(f"Sample width: {sample_width}")
        sample_rate = wf.getframerate()
        print(f"Sample rate: {sample_rate}")
        channels = wf.getnchannels()
        print(f"Channels: {channels}")
        pyaudio_format = self.Audio.get_format_from_width(sample_width)
        print(f"Format: {pyaudio_format}")
        self.send_info(pyaudio_format, sample_rate, channels)
        print("the connect is :", self.connected_)
        if self.connected_:
            nu_frames = wf.getnframes()
            print(f"No. of frames : {nu_frames}")
            wf.close()
            self.processing_init()
            print("Done sending wav")

    def processing_init(self):
        # Initialize Threads
        udpThread = threading.Thread(target=self.udpStream, daemon=True)
        udpThread.start()
        udpThread.join()

    def udpStream(self):
        self.stop1 = False
        wf = wave.open(self.source, 'rb')
        size = wf.getnframes()
        num_packets = int((size/self.chunks)+1)

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(num_packets):
            if self.stop1:
                break
            if self.pause2:
                while True:
                    if self.resume1:
                        self.pause2 = False
                        self.resume1 = False
                        break
                    continue
            udp.sendto(wf.readframes(self.chunks), self.server_address_1)
            progress_var.set(i)
            val = str(int((i/num_packets)*100))
            percentage_.set(val + "%")
            root.update()
            time.sleep(self.t)
        self.done__ = True
        print("closing socket")
        udp.close()


    def send_info(self, format_py, sample_rate, channels):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        print("Connecting to {}".format(self.server_address))
        try:
            sock.connect(self.server_address)
        except:
            print("Can't connect target machine refuse.")
            self.connected_ = False
        else:
            self.connected_ = True
        if self.connected_:
            file_info = struct.pack(">iii", format_py, sample_rate, channels)
            sock.send(file_info)
            print("format is send!")
            sock.close()

    def stop_play(self):
        self.stop1 = True
        self.done__ = True

    def resume_play(self):
        self.done__ = False
        self.resume1 = True
    
    def pause_play(self):
        self.pause2 = True
        self.done__ = True


class Client3_Send(object):
    def __init__(self, ip=None, port=None, ip2=None, port2=None):
        super(Client3_Send, self).__init__()

        self.success_connect_1 = True
        self.success_connect_2 = True
        self.keep_running = True
        
        if ip is not None and port is not None:
            self.ip = ip
            self.port = int(port)+1
            self.server_address = (self.ip, self.port)
        else:
            self.server_address = None
        if ip2 is not None and port2 is not None:
            self.ip2 = ip2
            self.port2 = int(port2)+1
            self.server_address_2 = (self.ip2, self.port2)
        else:
            self.server_address_2 = None

        self.hourbell = Client_hourbell()


    def running_all(self, name):
        if os.path.exists('sound.txt'):
            w = open('sound.txt', 'r+')
            w = w.read()
            source = json.loads(w)
        else:
            t1 = item_source.get()
            source = {**t1}
        source = source[name]
        self.source = source
        t1 = threading.Thread(target=self.server1_operate, daemon=True)
        t2 = threading.Thread(target=self.server2_operate, daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


    def server1_operate(self):
        print('connecting to {} port {}'.format(*self.server_address))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            sock.connect(self.server_address)
        except Exception as e:
            print(f'error--1: {e}')
            self.success_connect_1 = False
        else:
            self.success_connect_1 = True
            print("Successfully connect to 1")
        if self.success_connect_1:
            sock.setblocking(False)

            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, )
            # =========>
            # =========//////////
            self.main_operation()

    def server2_operate(self):
        try:
            print('connecting to {} port {}'.format(*self.server_address_2))
        except TypeError as e:
            pass
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock2.connect(self.server_address_2)
        except Exception as e:
            print(f'error--2: {e}')
            self.success_connect_2 = False
        else:
            self.success_connect_2 = True

        if self.success_connect_2:
            sock2.setblocking(False)
            print("Successfully connect to 2")
            # Set up the selector to watch for when the socket is ready
            # to send data as well as when there is data to read.
            mysel.register(sock2, selectors.EVENT_READ | selectors.EVENT_WRITE, )
            # =========>
            # =========//////////
            self.main_operation()


    def main_operation(self):
        if self.keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                connection = key.fileobj
                self.client_address = connection.getpeername()
                print('client({})'.format(self.client_address))
                if mask & selectors.EVENT_WRITE:
                    self.service_operate(connection)


    def service_operate(self, conn):
        data = b"l01ik20apBjok0q3k2oCo3k3Piz3i"
        pack_data = struct.pack(">29sii", data, 10390, 209340)
        conn.sendall(pack_data)
        if pack_data:
            address_1 = conn.getpeername()
            ip_add = address_1[0]
            port_add = address_1[1]
            source = self.source
            print("sending data")
            self.hourbell.operator_wav(ip_add,port_add, source)
            #w.operator_wav()
            mysel.unregister(conn)
            conn.close()


class Client_hourbell(object):
    def __init__(self):
        super(Client_hourbell, self).__init__()
        self.resume_play()
        self.done = False

        self.frames = []


        self.chunks = 1000
        self.t = 0.00125
        self.Audio = pyaudio.PyAudio()
        self.connected_ = False
        
        self.stop1 = False
        self.pause2 = False
        self.resume1 = False
        self.done__ = False

    def operator_wav(self,ip, port, source):
        self.ip = ip
        self.port = port+1
        self.port_1 = port+2
        self.server_address = (self.ip, self.port)
        self.server_address_1 = (self.ip, self.port_1)
        self.source = source
        wf = wave.open(self.source, 'rb')
        sample_width = wf.getsampwidth()
        print(f"Sample width: {sample_width}")
        sample_rate = wf.getframerate()
        print(f"Sample rate: {sample_rate}")
        channels = wf.getnchannels()
        print(f"Channels: {channels}")
        pyaudio_format = self.Audio.get_format_from_width(sample_width)
        print(f"Format: {pyaudio_format}")
        self.send_info(pyaudio_format, sample_rate, channels)
        print("the connect is :", self.connected_)
        if self.connected_:
            nu_frames = wf.getnframes()
            print(f"No. of frames : {nu_frames}")
            wf.close()
            self.processing_init()
            print("Done sending wav")

    def processing_init(self):
        # Initialize Threads
        udpThread = threading.Thread(target=self.udpStream, daemon=True)
        udpThread.start()
        udpThread.join()

    def udpStream(self):
        self.stop1 = False
        wf = wave.open(self.source, 'rb')
        size = wf.getnframes()
        num_packets = int((size/self.chunks)+1)

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(num_packets):
            if self.stop1:
                break
            if self.pause2:
                while True:
                    if self.resume1:
                        self.pause2 = False
                        self.resume1 = False
                        break
                    continue
            udp.sendto(wf.readframes(self.chunks), self.server_address_1)
            progress_var.set(i)
            val = str(int((i/num_packets)*100))
            percentage_.set(val + "%")
            root.update()
            time.sleep(self.t)
        self.done__ = True
        print("closing socket")
        udp.close()


    def send_info(self, format_py, sample_rate, channels):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        print("Connecting to {}".format(self.server_address))
        try:
            sock.connect(self.server_address)
        except:
            print("Can't connect target machine refuse.")
            self.connected_ = False
        else:
            self.connected_ = True
        if self.connected_:
            file_info = struct.pack(">iii", format_py, sample_rate, channels)
            sock.send(file_info)
            print("format is send!")
            sock.close()

    def stop_play(self):
        self.stop1 = True
        self.done__ = True

    def resume_play(self):
        self.done__ = False
        self.resume1 = True
    
    def pause_play(self):
        self.pause2 = True
        self.done__ = True

def center_window(app, w=300, h=200):
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        app.geometry('%dx%d+%d+%d' % (w, h, x, y))


if __name__ == '__main__':
    root = tk.Tk()
    ip_input = tk.StringVar(root)
    ip_input_1 = tk.StringVar(root)
    port_input = tk.IntVar(root)
    port_input_1 = tk.IntVar(root)
    bool1 = tk.BooleanVar(root)
    bool2 = tk.BooleanVar(root)
    bool3 = tk.BooleanVar(root)
    live_run = tk.BooleanVar(root)
    #------
    _conn1 = tk.StringVar(root)
    _conn2 = tk.StringVar(root)
    _conn3 = tk.StringVar(root)
    _conn4 = tk.StringVar(root)
    progress_var = tk.DoubleVar(root)
    percentage_ = tk.StringVar(root)
    item_source = tk.StringVar(root)
    app = MainWindow(root)
    root.mainloop()
