import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

class Viewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        rootHeight = parent.winfo_height()
        rootWidth = parent.winfo_width()
        # create main frames
        self.color_frame = ttk.Frame(self, height=int(0.05*rootHeight), width=rootWidth)
        self.images_frame = ttk.Frame(self, height=int(0.9*rootHeight), width=rootWidth)
        self.buttons_frame = ttk.Frame(self, height=int(0.05*rootHeight), width=rootWidth)
        #Extra space configration
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        #Place frames
        self.color_frame.grid(row=0,column=0, sticky='nsew')
        self.images_frame.grid(row=1, column=0, sticky='nsew')
        self.buttons_frame.grid(row=2, column=0, sticky='nsew')
        #Create color bar
        self.create_colorbar(self.color_frame)
        #Create image figures
        self.create_images(self.images_frame)
        #Create buttons
        self.create_buttons(self.buttons_frame)

    def create_colorbar(self, parent):
        self.max_c= tk.IntVar()
        self.color_bar = tk.Scale(parent, label= "max_v", orient='horizontal',
                                   variable=self.max_c)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.color_bar.grid(row=0,column=0, sticky='nsew')
        
    def create_images(self, parent):
        rootHeight = parent.winfo_reqheight()
        rootWidth = parent.winfo_reqwidth()
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        self.tax_frame = ttk.Frame(parent, height=int(round(rootHeight/2)),
                                    width=int(round(rootWidth/3)))
        self.co_frame = ttk.Frame(parent, height=int(round(rootHeight/2)),
                                   width=int(round(rootWidth/3)))
        self.sg_frame = ttk.Frame(parent, height=int(round(rootHeight/2)),
                                   width=int(round(rootWidth/3)))
        #Transaxial view frame
        self.tax_frame.rowconfigure(0, weight=1)
        self.tax_frame.rowconfigure(1, weight=1)
        self.tax_frame.columnconfigure(0, weight=1)
        # #Coronary view frame
        self.co_frame.rowconfigure(0, weight=1)
        self.co_frame.rowconfigure(1, weight=1)
        self.co_frame.columnconfigure(0, weight=1)
        # #Saggital view frame
        self.sg_frame.rowconfigure(0, weight=1)
        self.sg_frame.rowconfigure(1, weight=1)
        self.sg_frame.columnconfigure(0, weight=1)
        #Position frames
        self.tax_frame.grid(row=0, column=0, sticky='nsew')
        self.co_frame.grid(row=0, column=1, sticky='nsew')
        self.sg_frame.grid(row=0, column=2, sticky='nsew')
        #Create labels
        self.tax_lbl = tk.Label(self.tax_frame, text="Transaxial", width=int(round(rootWidth/3)))
        self.co_lbl = tk.Label(self.co_frame, text="Coronal", width=int(round(rootWidth/3)))
        self.sg_lbl = tk.Label(self.sg_frame, text="Saggital", width=int(round(rootWidth/3)))
        #Create images
        self.tax_img = tk.Canvas(self.tax_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        self.co_img = tk.Canvas(self.co_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        self.sg_img = tk.Canvas(self.sg_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        #Position labels
        self.tax_lbl.grid(row=0,column=0)
        self.co_lbl.grid(row=0,column=0)
        self.sg_lbl.grid(row=0,column=0)
        #Posiiton images
        self.tax_img.grid(row=1, column=0, sticky='nsew')
        self.co_img.grid(row=1, column=0, sticky='nsew')
        self.sg_img.grid(row=1, column=0, sticky='nsew')

    def update_tax_img(self, img):
        w = self.tax_img.winfo_reqwidth()
        h = self.tax_img.winfo_reqheight()
        #Convert to color palette
        rgb_img= (plt.get_cmap('CMRmap')(img)*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('ta_pic.png')
        self.tax_ph_image = tk.PhotoImage(file='./ta_pic.png', width=w, height=h)
        self.tax_img.create_image(0, 0, anchor=tk.NW, image=self.tax_ph_image)

    def update_co_img(self, img):
        w = self.co_img.winfo_reqwidth()
        h = self.co_img.winfo_reqheight()
        #Convert to color palette
        rgb_img= (plt.get_cmap('CMRmap')(img)*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('co_pic.png')
        self.co_ph_image = tk.PhotoImage(file='./co_pic.png',width=w, height=h)
        self.co_img.create_image(0, 0, anchor=tk.NW, image=self.co_ph_image)

    def update_sg_img(self, img):
        w = self.sg_img.winfo_reqwidth()
        h = self.sg_img.winfo_reqheight()
        #Convert to color palette
        rgb_img= (plt.get_cmap('CMRmap')(img)*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('sg_pic.png')
        self.sg_ph_image = tk.PhotoImage(file='./sg_pic.png',width=w, height=h)
        self.sg_img.create_image(0, 0, anchor=tk.NW, image=self.sg_ph_image)


    def create_buttons(self, parent):
        self.progress_bar = ttk.Button(parent,text="Progress")
        self.save_button = ttk.Button(parent, text="Save")
        self.prev_button = ttk.Button(parent, text="Previous study")
        self.next_button = ttk.Button(parent, text="Next study")
        #Position buttons
        self.progress_bar.grid(row=0, column=0, sticky="nsew")
        self.save_button.grid(row=0, column=1,sticky="nsew")
        self.prev_button.grid(row=0, column=2, sticky="nsew")
        self.next_button.grid(row=0, column=3, sticky="nsew")

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def save_button_clicked(self):
        """
        Handle button click event
        :return:
        """
        if self.controller:
            self.controller.save(self.email_var.get())

# HEIGHT= 600
# WIDTH= 600
# root = tk.Tk()
# root.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+50+50")  # width x height + x + y
# root.grid_rowconfigure(0, weight=1)
# root.grid_columnconfigure(0, weight=1)
# viewer = Viewer(root)
# viewer.grid(row=0,column=0)
# root.mainloop()