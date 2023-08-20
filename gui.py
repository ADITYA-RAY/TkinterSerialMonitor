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

customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Serial Monitor - By Aditya Ray")
        self.geometry(f"{1400}x{720}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        plt.style.use({
            'axes.facecolor': '#1C1C1C',
            'axes.edgecolor': 'gray',
            'axes.labelcolor': 'white',
            'text.color': 'white',
            'xtick.color': 'tab:blue',
            'ytick.color': 'tab:blue',
            'grid.color': 'gray',
            'figure.facecolor': '#1a1a1a',
            'figure.edgecolor': '#1a1a1a',
            'savefig.facecolor': '#1a1a1a',
            'savefig.edgecolor': '#1a1a1a',
        })

        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=1,rowspan=2,columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.sidebar_frame = customtkinter.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, columnspan=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Python Serial Monitor", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,values=["/dev/ttyACM0"])
        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=10)
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,values=[
               "300","600","1200","2400","4800","9600","14400","19200","28800","38400","56000","57600","115200","128000","256000"])
        self.optionmenu_2.grid(row=2, column=0, padx=20, pady=10)
        self.main_button_2 = customtkinter.CTkButton(master=self.sidebar_frame,command=threading.Thread(target=self.handle_connect).start,text = "Connect", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Channel 1","Channel 2","all channels"])
        self.optionmenu_3.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_frame.grid_columnconfigure(0)
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=280)
        self.textbox.grid(row=4, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter Message")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent",text="Send", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")  
        self.optionmenu_1.set("Device")
        self.optionmenu_2.set("Baud Rate")
        self.optionmenu_3.set("Select Channel")

    def open_input_dialog_event(self):
        messagebox.showerror('Python Error', 'Incorrect Device or Baud Rate!')

    def handle_connect(self):
        self.x_axis = 0
        plt.ion()
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
                        if self.optionmenu_3.get() == "all":
                            self.showChannel = [1,1]
                        elif self.optionmenu_3.get() == "1":
                            self.showChannel = [1,0]
                        else:
                            self.showChannel =[0,1]
                        print(self.showChannel)
                        if self.showChannel[i]:
                            plt.plot(self.numx[i],self.numy[i],self.colors[i])
                        self.fig.canvas.draw()     
                        self.fig.canvas.flush_events()

if __name__ == "__main__":
    app = App()
    app.mainloop()