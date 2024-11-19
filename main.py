import tkinter as tk
from model import Model
from Viewer import Viewer
from Controller import Controller

def login_screen():
    root=tk.Tk()

    # setting the windows size
    root.geometry("600x400")
    name_var=tk.StringVar()
    
    # defining a function that will
    # get the name and password and 
    # print them on the screen
    def submit():
        name=name_var.get()
        print("The name is : " + name)
        root.destroy()
        
    # creating a label for 
    # name using widget Label
    name_label = tk.Label(root, text = 'Username', font=('calibre',10, 'bold'))
    
    # creating a entry for input
    # name using widget Entry
    name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))
    
    # creating a button using the widget 
    # Button that will call the submit function 
    sub_btn=tk.Button(root,text = 'Submit', command = submit)
    
    # placing the label and entry in
    # the required position using grid
    # method
    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    sub_btn.grid(row=1,column=1)
    
    # performing an infinite loop 
    # for the window to display
    root.mainloop()
    return name_var.get()


user_name = login_screen()
dir_name = ".//Results//"
N_SLICES = 128
HEIGHT= 800
WIDTH= 1000
root = tk.Tk()
root.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+50+50")  # width x height + x + y
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.update()
#Viewer. Model and controller
viewer = Viewer(root)
viewer.grid(row=0,column=0)
model = Model()
controller = Controller(user_name, model, viewer, dir_name)
viewer.set_controller(controller)
viewer.create_widgets(N_SLICES)
controller.set_dir(dir_name)

root.mainloop()

