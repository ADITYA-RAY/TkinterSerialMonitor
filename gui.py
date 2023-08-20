import tkinter as tk

class gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tkinter Serial Monitor")
        self.window.geometry("800x600")
        self.window.mainloop()
        
    
class comGui():
    def __init__(self,root):
        self.com = LabelFrame(root,text="Communication Manager" ,padx=5,pady=5)
        self.label_com = Label(self.com, text ="Device: ",width=200)
    
    def publish(self):
        self.com.grid(row=0,column=0)





if __name__ == "__main__":
    main = gui()
    comGui(main)


