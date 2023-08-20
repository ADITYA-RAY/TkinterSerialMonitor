import tkinter
import tkinter.messagebox
import customtkinter
from backend import backend 
from tkinter import messagebox
import threading
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
# plt.switch_backend('agg')


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        

        # configure window
        self.title("Tkinter Serial Monitor")
        self.geometry(f"{1400}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_columnconfigure(0,weight = 0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, columnspan=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PySerial Monitor", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["/dev/ttyACM0"])
        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=10)
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=[
               "300","600","1200","2400","4800","9600","14400","19200","28800","38400","56000","57600","115200","128000","256000"])
        self.optionmenu_2.grid(row=2, column=0, padx=20, pady=10)
        self.main_button_2 = customtkinter.CTkButton(master=self.sidebar_frame,command=threading.Thread(target=self.handle_connect).start,text = "Connect", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0)

        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=280)
        self.textbox.grid(row=4, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

       
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
        #                                                        command=self.change_scaling_event)
        # self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")  
       
        self.appearance_mode_optionemenu.set("Dark")
        # self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Device")
        self.optionmenu_2.set("Baud Rate")

    def open_input_dialog_event(self):
        messagebox.showerror('Python Error', 'Incorrect Device or Baud Rate!')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def handle_connect(self):
        self.x_axis = 0
        plt.ion()
        self.fig = plt.figure()
        self.numx = [[0]*2]*2
        self.numy = [[0]*2]*2
        self.colors=["r-","b-"]
        device = self.optionmenu_1.get()
        bd = self.optionmenu_2.get()
        if  device == "Device" or bd == "Baud Rate": 
            self.open_input_dialog_event()
        else:
            process = backend()
            process.connect(device,bd)
           
            while True:
                data = process.getData()
                if data:
                    self.x_axis+=1
                    self.textbox.insert('1.0',  str(data) + "\n")
                    for i in range(len(data)):
                        self.numx[i] = [self.numx[i][1],self.x_axis]
                        self.numy[i] = [self.numy[i][1],int(data[i])]
                        plt.plot(self.numx[i],self.numy[i],self.colors[i])
                        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                        self.fig.canvas.draw()     
                        self.fig.canvas.flush_events()
                        self.fig.get_tk_widget().pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()