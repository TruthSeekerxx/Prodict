import tkinter as tk
import numpy as np
import client_info as ci
import threading
import time


root = tk.Tk()
root.geometry('400x400')
root.title('Prodict')
root.resizable(False, False)


my_canvas = tk.Canvas(root, width=400, height=400)
my_canvas.pack()

try:
    bg = tk.PhotoImage(file='background_image.png')
    my_canvas.create_image(200,200,image=bg)
except:
    pass






font_1 = '#C6C6C6'
font_2 = '#2B3249'

my_canvas.create_rectangle(0,0,180,180, fill=font_2)
my_canvas.create_rectangle(220,0,400,180, fill=font_2)
my_canvas.create_rectangle(0,220,180,400, fill=font_2)
my_canvas.create_rectangle(220,220,400,400, fill=font_2)
my_canvas.create_line(0,30,180,30,fill='white')
my_canvas.create_line(0,250,180,250,fill='white')
my_canvas.create_line(221,30,400,30,fill='white')
my_canvas.create_line(221,250,400,250,fill='white')
my_canvas.create_line(90,0,90,180,fill='white')



my_canvas.create_text(30,50, text='Darius',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(30,65, text='Kayn',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(30,80, text='Lux',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(30,95, text='Caitlyn',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(30,110, text='Braum',fill=font_1,font=('KacstDigital',9),anchor='w')

my_canvas.create_text(110,50, text='Garen',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(110,65, text='Fiddlesticks',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(110,80, text='Zed',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(110,95, text='Karthus',fill=font_1,font=('KacstDigital',9),anchor='w')
my_canvas.create_text(110,110, text='Yummi',fill=font_1,font=('KacstDigital',9),anchor='w')

my_canvas.create_text(45,20, text='US',fill=font_1,font=('KacstDigital',10))
my_canvas.create_text(135,20, text='THEM',fill=font_1,font=('KacstDigital',10))
my_canvas.create_text(310,20, text='OPTIONS',fill=font_1,font=('KacstDigital',10))
my_canvas.create_text(90,240, text='PROBABILITY OF WIN',fill=font_1,font=('KacstDigital',10))
my_canvas.create_text(310,240, text='REASONS',fill=font_1,font=('KacstDigital',10))



x = str(round(np.random.normal(loc=50,scale=4),2))+'%'
my_canvas.create_text(90,310, text=x,fill=font_1,font=('KacstDigital',20))
my_canvas.create_text(230,270, text='- bad midlane pick',fill=font_1,font=('KacstDigital',8),anchor='w')
my_canvas.create_text(230,285, text='- support is tilted',fill=font_1,font=('KacstDigital',8),anchor='w')
my_canvas.create_text(230,300, text='- first time darius',fill=font_1,font=('KacstDigital',8),anchor='w')



var = tk.IntVar()
var_1 = tk.IntVar()
var_2 = tk.IntVar()
var_3 = tk.IntVar()
var_4 = tk.IntVar()
var_5 = tk.IntVar()
x = tk.Checkbutton(my_canvas,text='match history',variable=var,bg=font_2,fg=font_1,activebackground=font_2)
x.place(x=230,y=40)
x = tk.Checkbutton(my_canvas,text='champion win rates',variable=var_1,bg=font_2,fg=font_1,activebackground=font_2)
x.place(x=230,y=60)
x = tk.Checkbutton(my_canvas,text='player champion winrate',variable=var_2,bg=font_2,fg=font_1,activebackground=font_2)
x.place(x=230,y=80)
x = tk.Checkbutton(my_canvas,text='their team synergy',variable=var_3,bg=font_2,fg=font_1,activebackground=font_2)
x.place(x=230,y=100)
x = tk.Checkbutton(my_canvas,text='our team synergy',variable=var_4,bg=font_2,fg=font_1,activebackground=font_2)
x.place(x=230,y=120)
x = tk.Checkbutton(my_canvas,text='counterpicks',variable=var_5,bg=font_2,fg=font_1,activebackground=font_2)
x.place(x=230,y=140)


information = my_canvas.create_text(250,380, text='Open the client',fill=font_1,font=('KacstDigital',10),anchor='w')





def thread_client():
    ci.check_client()
    if ci.check_client.yo=='Client not open':
        ci.check_client()
        print(ci.check_client.yo)
        thread_client.t = threading.Timer(1, thread_client)
        thread_client.t.daemon=True
        thread_client.t.start()
    else:
        print('cancelling')
        my_canvas.itemconfig(information,text='Get into champion select')
        ci.get_passwords()
        thread_select()
        
def thread_select():
    ci.check_Cselect()
    if ci.check_Cselect.yo=='Not in champion select':
        ci.check_Cselect()
        print(ci.check_Cselect.yo)
        thread_select.t = threading.Timer(1, thread_select)
        thread_select.t.daemon=True
        thread_select.t.start()
    else:
        print('in champ select')







thread_client()



root.mainloop()

try:
    print('thread_select-stop')
    for i in range(10):
        thread_select.t.cancel()
        time.sleep(0.1)
except:
    print('thread_client-stop')
    for i in range(10):
        thread_client.t.cancel()
        time.sleep(0.1)



