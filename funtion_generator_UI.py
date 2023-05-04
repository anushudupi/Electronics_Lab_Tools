import tkinter
import tkinter.messagebox
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import  sin
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import serial.tools.list_ports
import serial
ports=(list(serial.tools.list_ports.comports()))
ports=(list(serial.tools.list_ports.comports()))
for i in range(len(ports)):
   ports[i]=((str(ports[i])).split(' '))[0]
print(ports)
global ser
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

options_map = {
    3: "Square Wave",
    2: "Sine Wave",
    1: "Triangular Wave",
}

multiplier={
    "Hz" : 1,
    "KHz" : 1000,
    "MHz" : 10**6,
    "GHz" : 10**9
}

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        font_q=customtkinter.CTkFont( size=15)
        var = customtkinter.IntVar()
        var_hz = customtkinter.IntVar()
        var.trace("w", lambda *args: highlight_option(var.get()))

        def get_input():
            option = var.get()
            num = num_entry.get()
            mult=var_hz.get()
            
            
            if mult==1:
                try:
                    ser.write(bytes(str(f'{option}:{num}'), 'utf-8'))
                    #ser.write(b'\n')
                    result_label.configure(text=f"{options_map[option]} of {num} Hz ", pady=10)
                except:   
                   result_label.configure(text=f"Port not connected", pady=10)

            elif mult==2:
                try:
                    ser.write(bytes(str(f'{option}:{str(num*1000)}'), 'utf-8'))
                    #ser.write(b'\n')                    
                    result_label.configure(text=f"{options_map[option]} of {num} KHz ", pady=10)
                except:
                    result_label.configure(text=f"Port not connected", pady=10)  
            else:
                 try:
                    ser.write(bytes(f'{option}:{num*1000000}', 'utf-8'))
                    #ser.write(b'\n')
                    result_label.configure(text=f"{options_map[option]} of {num} MHz", pady=10)
                 except:
                    result_label.configure(text=f"Port not connected", pady=10)    

        def highlight_option(option):
            if option == 1:
                #option1_button.configure(relief=customtkinter.SUNKEN)
                option1_button.config(state=customtkinter.FLAT)
                option2_button.config(relief=customtkinter.RAISED)
                option3_button.config(relief=customtkinter.RAISED)
            elif option == 2:
                option1_button.config(relief=customtkinter.RAISED)
                option2_button.config(relief=customtkinter.SUNKEN)
                option3_button.config(relief=customtkinter.RAISED)
            elif option == 3:
                option1_button.config(relief=customtkinter.RAISED)
                option2_button.config(relief=customtkinter.RAISED)
                option3_button.config(relief=customtkinter.SUNKEN)
            # configure window
        self.title("FUNCTION GENERATOR")
        self.geometry(f"{800}x{700}")

        # configure grid layout (4x2)
        self.grid_columnconfigure((1), weight=1)
        #self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        
        var = customtkinter.IntVar()
        var_hz = customtkinter.IntVar()
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=265, corner_radius=20,border_width=3)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4,padx=15,pady=15,sticky="nsew")
        self.sidebar_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="MENU", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.port_label = customtkinter.CTkLabel(self.sidebar_frame,font=font_q, text="Select Port:", anchor="w")
        self.port_label.grid(row=1, column=0, padx=10, pady=(10,0))
        self.menu=customtkinter.CTkOptionMenu(self.sidebar_frame,values=list(ports),command=self.port)
        self.menu.grid(row=2,column=0,padx=10,pady=(5,10))
        self.menu.set("Data Port")

        self.vol1_label = customtkinter.CTkLabel(self.sidebar_frame, font=font_q, text="Voltage:", anchor="w")
        self.vol1_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.entry1 = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="peak-peak")
        self.entry1.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.entry2 = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="offset")
        self.entry2.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, font=font_q, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System","Light", "Dark" ],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, font=font_q,text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))



        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, rowspan=7,pady=15,padx=(0,15), sticky="nsew")
        self.main_frame.grid_rowconfigure((1,2,3,4,5,6,), weight=1)
        self.main_frame.grid_columnconfigure((0,1,2),weight=1)
        
        wv_label = customtkinter.CTkLabel(self.main_frame, font=customtkinter.CTkFont(size=20,weight="bold"), text="FUNCTION GENERATOR")
        wv_label.grid(row=0,column=0,columnspan=3,pady=10,sticky="nsnew")
        # Icons for sine, trianular and square"""
        option1_icon = ImageTk.PhotoImage(Image.open("triangular.png").resize((100, 100)))
        option2_icon = ImageTk.PhotoImage(Image.open("sine.png").resize((100, 100)))
        option3_icon = ImageTk.PhotoImage(Image.open("square.png").resize((100, 100)))
        
        option3_button = customtkinter.CTkButton(self.main_frame,image=option3_icon, font=font_q, text="Square", command=lambda: var.set(3))
        option2_button = customtkinter.CTkButton(self.main_frame,image=option2_icon, font=font_q, text="Sine", command=lambda: var.set(2))
        option1_button = customtkinter.CTkButton(self.main_frame,image=option1_icon, font=font_q, text="Triangular", command=lambda: var.set(1))

        option1_button.grid(row=1,column=0,padx=15,pady=(20,30))
        option2_button.grid(row=1,column=1,pady=(20,30))
        option3_button.grid(row=1,column=2,padx=15,pady=(20,30))

        R1 = customtkinter.CTkRadioButton(self.main_frame, font=font_q, text="Hz", variable=var_hz, value=1).grid(row=4,column=0,padx=10,pady=10)
        R2 = customtkinter.CTkRadioButton(self.main_frame, font=font_q, text="K-Hz", variable=var_hz, value=2).grid(row=4,column=1,padx=10,pady=10)
        R3 = customtkinter.CTkRadioButton(self.main_frame, font=font_q, text="M-Hz", variable=var_hz, value=3).grid(row=4,column=2,padx=10,pady=10)

        #Integer Input for frequency
        num_label = customtkinter.CTkLabel(self.main_frame, font=font_q, text="FREQUENCY:")
        num_entry = customtkinter.CTkEntry(self.main_frame, width=200, font=font_q, placeholder_text="Enter the frequency")
        num_label.grid(row=2,column=0,columnspan=3)
        num_entry.grid(row=3,column=0,columnspan=3,pady=10)








        submit_button = customtkinter.CTkButton(self.main_frame, font=font_q, text="Generate", command=get_input)
        submit_button.grid(row=5,column=0,columnspan=3,padx=20,pady=(10,10))
 
        result_label = customtkinter.CTkLabel(self.main_frame, font=font_q,text="")
        result_label.grid(row=6,column=0,columnspan=3,padx=20,pady=(10,10))

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def port(self,name:str):
        global ser
        try:
             ser = serial.Serial(port=name, baudrate=115200, timeout=1)
        except:
            print('port not available')
            pass    


    
    #Highlighting the selected option
    
if __name__ == "__main__":
    app = App()
    app.mainloop()