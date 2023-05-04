
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter
import tkinter as tk
import numpy as np
import threading
import queue
import serial
import matplotlib.pyplot as plt
import matplotlib.style as style
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

# Initialize the data queue
import serial.tools.list_ports
ports=(list(serial.tools.list_ports.comports()))
for i in range(len(ports)):
   ports[i]=((str(ports[i])).split(' '))[0]

data_queue = queue.Queue(maxsize=2)

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
def data_generator():
    pattern="\nabcdefg"
    n = 10000
    ser = serial.Serial('COM5',1000000000)
    i=0
    while True:
            try:
               data = ser.read().decode() # Read a single character from the serial port
            except:
                pass
            if data == pattern[i]: # Check if the character matches the first character in the pattern
                
                i=i+1
                if i==8: # If all characters in the pattern have been matched
                    
                    bytes = ser.read(8000) # Read up to 1024 bytes
                    #print("pass")
                    data=np.frombuffer(bytes, dtype=np.uint8)
                    data_queue.put(data)
                    ser.close()
                    i=0
                    ser.open()
                    
    

                #arr = np.frombuffer(bytes, dtype=np.int8)       
            else:
                
                i=0  


# Start the data generator thread
thread = threading.Thread(target=data_generator)
thread.daemon = True
thread.start()




customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

root1 = customtkinter.CTk()
root1.title("Dynamic Plot")


root1.grid_rowconfigure(0, weight=1)
root1.grid_columnconfigure(1, weight=1)

frame0 = customtkinter.CTkFrame(master=root1)
frame0.grid(row=0,column=0,padx=(20,20), pady=20,sticky="nsew")
frame0.grid_rowconfigure(4, weight=1)

port_label = customtkinter.CTkLabel(frame0, text="Select Port:", anchor="w")
port_label.grid(row=0, column=0, padx=10, pady=(10,0))
menu=customtkinter.CTkOptionMenu(frame0,values=list(ports))
menu.grid(row=1,column=0,padx=10,pady=(5,10))
menu.set("Data Port")

appearance_mode_label = customtkinter.CTkLabel(frame0, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=10, pady=5)

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(frame0, values=["System","Light", "Dark" ],command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0,padx=10,pady=(0,10))

scaling_label = customtkinter.CTkLabel(frame0,text="UI Scaling:", anchor="w")
scaling_label.grid(row=7, column=0, padx=10, pady=(0,5))
scaling_optionemenu = customtkinter.CTkOptionMenu(frame0, values=["70%","80%", "90%", "100%", "110%", "120%","130%"],
                                                               command=change_scaling_event)
scaling_optionemenu.grid(row=8, column=0, padx=10, pady=(0, 10))
scaling_optionemenu.set("100%")



#color_mode_label = customtkinter.CTkLabel(frame0, text="Appearance Mode:", anchor="w")
#color_mode_label.grid(row=7, column=0, padx=20, pady=(0,10))
#color_mode_optionemenu = customtkinter.CTkOptionMenu(frame0, values=["Blue", "Dark-blue", "Green"],command=change_color_mode_event)
#color_mode_optionemenu.grid(row=8, column=0,padx=20,pady=(0,20))

frame1 = customtkinter.CTkFrame(master=root1 )
frame1.grid(row=0,column=1,pady=(20,0),sticky="nsew")
plt.style.use("ggplot")
fig = Figure()
ax = fig.add_subplot(111)
ax.set_title("WaveForm")
ax.set_ylim([0,300])
ax.set_xlim([0,8000])
line, = ax.plot(np.random.randn(8000))
canvas = FigureCanvasTkAgg(fig, master=frame1)
toolbar = NavigationToolbar2Tk(canvas,frame1)
toolbar.update()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


frame2=customtkinter.CTkFrame(master=root1)
frame2.grid(row=0,column=2,padx=(20,20),pady=20,sticky="nsew")
frame2.grid_rowconfigure(4, weight=1)


def update_plot():
    
    try: 
        data = data_queue.get_nowait()
        #print(data)
        #ax.set_xlim([0,4000])
        line.set_ydata(data)
        canvas.draw()
        canvas.flush_events()
    except queue.Empty:
        pass 
    root1.after(1, update_plot)   

    



update_plot()
root1.mainloop()
