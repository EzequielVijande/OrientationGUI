import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


SCORES = ["Completely", "A lot", "Somewhat", "Slightly", "Nothing"]
CMAP = 'gray_r'
GUIDE_LINE_C = "red"

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

    def create_widgets(self, n_slices):
        #Create color bar
        self.create_scales(self.color_frame)
        #Create image figures
        self.create_images(self.images_frame, n_slices)
        #Create buttons
        self.create_buttons(self.buttons_frame)

    def create_scales(self, parent):
        self.sat_percentage= tk.IntVar(value=80)
        self.color_bar = tk.Scale(parent, label= "Saturation", orient='horizontal', to=99,
                                   variable=self.sat_percentage, command=self.controller.update_imgs)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.color_bar.grid(row=0,column=0, sticky='nsew')
        
    def create_images(self, parent, n_slices):
        self.slice_n_shx = tk.IntVar(value=str(n_slices//2))
        self.slice_n_hla = tk.IntVar(value=str(n_slices//2))
        self.slice_n_vla = tk.IntVar(value=str(n_slices//2))
        
        rootHeight = parent.winfo_reqheight()
        rootWidth = parent.winfo_reqwidth()
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        self.shx_frame = ttk.Frame(parent, height=int(round(rootHeight/3)),
                                    width=int(round(rootWidth/3)))
        self.hla_frame = ttk.Frame(parent, height=int(round(rootHeight/3)),
                                   width=int(round(rootWidth/3)))
        self.vla_frame = ttk.Frame(parent, height=int(round(rootHeight/3)),
                                   width=int(round(rootWidth/3)))
        #Short axis view frame
        self.shx_frame.rowconfigure(0, weight=1)
        self.shx_frame.rowconfigure(1, weight=1)
        self.shx_frame.rowconfigure(2, weight=1)
        self.shx_frame.columnconfigure(0, weight=1)
        self.shx_frame.columnconfigure(1, weight=1)
        #Horizontal long axis view frame
        self.hla_frame.rowconfigure(0, weight=1)
        self.hla_frame.rowconfigure(1, weight=1)
        self.hla_frame.rowconfigure(2, weight=1)
        self.hla_frame.columnconfigure(0, weight=1)
        self.hla_frame.columnconfigure(1, weight=1)
        #Vertical long axis view frame
        self.vla_frame.rowconfigure(0, weight=1)
        self.vla_frame.rowconfigure(1, weight=1)
        self.vla_frame.rowconfigure(2, weight=1)
        self.vla_frame.columnconfigure(0, weight=1)
        self.vla_frame.columnconfigure(1, weight=1)

        #Position frames
        self.shx_frame.grid(row=0, column=0, sticky='nsew')
        self.hla_frame.grid(row=0, column=1, sticky='nsew')
        self.vla_frame.grid(row=0, column=2, sticky='nsew')

        #Short axis button frame
        self.shx_button_frame = ttk.Frame(self.shx_frame)
        self.shx_button_frame.rowconfigure(0, weight=1)
        self.shx_button_frame.rowconfigure(1, weight=1)
        self.shx_button_frame.columnconfigure(0, weight=1)
        self.shx_button_frame.columnconfigure(1, weight=1)
        #Horizontal long axis view frame
        self.hla_button_frame = ttk.Frame(self.hla_frame)
        self.hla_button_frame.rowconfigure(0, weight=1)
        self.hla_button_frame.rowconfigure(1, weight=1)
        self.hla_button_frame.columnconfigure(0, weight=1)
        self.hla_button_frame.columnconfigure(1, weight=1)
        #Vertical long axis view frame
        self.vla_button_frame = ttk.Frame(self.vla_frame)
        self.vla_button_frame.rowconfigure(0, weight=1)
        self.vla_button_frame.rowconfigure(1, weight=1)
        self.vla_button_frame.columnconfigure(0, weight=1)
        self.vla_button_frame.columnconfigure(1, weight=1)

        #Create images
        self.shx_img = tk.Canvas(self.shx_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootWidth/3)))
        self.hla_img = tk.Canvas(self.hla_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootWidth/3)))
        self.vla_img = tk.Canvas(self.vla_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootWidth/3)))
        #Sliders
        self.slice_bar_shx = tk.Scale(self.shx_frame, orient='horizontal', to=n_slices-1, label="Short axis",
                                   variable=self.slice_n_shx, command=self.controller.update_imgs)
        self.slice_bar_hla = tk.Scale(self.hla_frame, orient='horizontal', to=n_slices-1, label="HLA",
                                   variable=self.slice_n_hla, command=self.controller.update_imgs)
        self.slice_bar_vla = tk.Scale(self.vla_frame, orient='horizontal', to=n_slices-1, label="VLA",
                                   variable=self.slice_n_vla, command=self.controller.update_imgs)
        #Buttons
        self.shx_angle_lbl = ttk.Button(self.shx_button_frame, text="0°")
        self.hla_angle_lbl = ttk.Button(self.hla_button_frame, text="0°")
        self.vla_angle_lbl = ttk.Button(self.vla_button_frame, text="0°")
        self.shx_angle_lbl.grid(column=0)
        self.hla_angle_lbl.grid(column=0)
        self.vla_angle_lbl.grid(column=0)
        #Angle increment buttons
        self.shx_inc_angle = ttk.Button(self.shx_button_frame, text="↑",command=self.controller.increment_shx_angle)
        self.hla_inc_angle = ttk.Button(self.hla_button_frame, text="↑",command=self.controller.increment_hla_angle)
        self.vla_inc_angle = ttk.Button(self.vla_button_frame, text="↑",command=self.controller.increment_vla_angle)
        self.shx_inc_angle.grid(row=0, column=1, sticky='nsew')
        self.hla_inc_angle.grid(row=0, column=1, sticky='nsew')
        self.vla_inc_angle.grid(row=0, column=1, sticky='nsew')
        #Angle decrement buttons
        self.shx_dec_angle = ttk.Button(self.shx_button_frame, text="↓",command=self.controller.decrement_shx_angle)
        self.hla_dec_angle = ttk.Button(self.hla_button_frame, text="↓",command=self.controller.decrement_hla_angle)
        self.vla_dec_angle = ttk.Button(self.vla_button_frame, text="↓",command=self.controller.decrement_vla_angle)
        self.shx_dec_angle.grid(row=1, column=1, sticky='nsew')
        self.hla_dec_angle.grid(row=1, column=1, sticky='nsew')
        self.vla_dec_angle.grid(row=1, column=1, sticky='nsew')

        #Position sliders
        self.slice_bar_shx.grid(row=0,column=0, sticky='nsew')
        self.slice_bar_hla.grid(row=0,column=0, sticky='nsew')
        self.slice_bar_vla.grid(row=0,column=0, sticky='nsew')

        #Position button frame
        self.shx_button_frame.grid(row=0,column=1, sticky='nsew')
        self.hla_button_frame.grid(row=0,column=1, sticky='nsew')
        self.vla_button_frame.grid(row=0,column=1, sticky='nsew')

        #Position images
        self.shx_img.grid(row=1, sticky='nsew', columnspan=2)
        self.hla_img.grid(row=1, sticky='nsew', columnspan=2)
        self.vla_img.grid(row=1, sticky='nsew',columnspan=2)


    def update_shx_img(self, img, eps=1e-3):
        w = self.shx_img.winfo_reqwidth()
        h = self.shx_img.winfo_reqheight()
        rgb_img= (plt.get_cmap(CMAP)(img)*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('shx_pic.png')
        self.shx_ph_image = tk.PhotoImage(file='./shx_pic.png',width=w, height=h)
        self.shx_img.create_image(0, 0, anchor=tk.NW, image=self.shx_ph_image)
        self.shx_img.create_line(w/2,0,w/2,h, fill=GUIDE_LINE_C, width=0.5)
        self.shx_img.create_line(0,h/2,w,h/2, fill=GUIDE_LINE_C, width=0.5)
    
    def update_hla_img(self, img, eps=1e-3):
        w = self.hla_img.winfo_reqwidth()
        h = self.hla_img.winfo_reqheight()
        rgb_img= (plt.get_cmap(CMAP)(img)*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('hla_pic.png')
        self.hla_ph_image = tk.PhotoImage(file='./hla_pic.png',width=w, height=h)
        self.hla_img.create_image(0, 0, anchor=tk.NW, image=self.hla_ph_image)
        self.hla_img.create_line(w/2,0,w/2,h, fill=GUIDE_LINE_C, width=0.5)
        self.hla_img.create_line(0,h/2,w,h/2, fill=GUIDE_LINE_C, width=0.5)

    def update_vla_img(self, img, eps=1e-3):
        w = self.vla_img.winfo_reqwidth()
        h = self.vla_img.winfo_reqheight()
        rgb_img= (plt.get_cmap(CMAP)(img)*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('vla_pic.png')
        self.vla_ph_image = tk.PhotoImage(file='./vla_pic.png',width=w, height=h)
        self.vla_img.create_image(0, 0, anchor=tk.NW, image=self.vla_ph_image)
        self.vla_img.create_line(w/2,0,w/2,h, fill=GUIDE_LINE_C, width=0.5)
        self.vla_img.create_line(0,h/2,w,h/2, fill=GUIDE_LINE_C, width=0.5)

    def create_buttons(self, parent):
        self.prev_button = ttk.Button(parent, text="Previous study", command=self.controller.prev_study)
        self.next_button = ttk.Button(parent, text="Next study", command=self.controller.next_study)
        self.progress_bar = ttk.Label(parent, text="Progress: ")
        #Position buttons
        self.prev_button.grid(row=0, column=0, sticky="nsew")
        self.next_button.grid(row=0, column=1, sticky="nsew")
        self.progress_bar.grid(row=0, column=2, sticky="nsew")

    def disable_next_button(self):
        self.next_button.config(state=tk.DISABLED)

    def enable_next_button(self):
        self.next_button.config(state=tk.NORMAL)

    def disable_prev_button(self):
        self.prev_button.config(state=tk.DISABLED)

    def enable_prev_button(self):
        self.prev_button.config(state=tk.NORMAL)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
