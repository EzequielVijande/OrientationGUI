import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


SCORES = ["Completely", "A lot","Somewhat", "Slightly", "Nothing"]

class Viewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        rootHeight = parent.winfo_height()
        rootWidth = parent.winfo_width()
        # create main frames
        self.color_frame = ttk.Frame(self, height=int(0.2*rootHeight), width=rootWidth)
        self.images_frame = ttk.Frame(self, height=int(0.7*rootHeight), width=rootWidth)
        self.buttons_frame = ttk.Frame(self, height=int(0.1*rootHeight), width=rootWidth)
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
        self.create_scales(self.color_frame, n_slices)
        #Create image figures
        self.create_images(self.images_frame)
        #Create buttons
        self.create_buttons(self.buttons_frame)

    def create_scales(self, parent, n_slices):
        self.sat_percentage= tk.IntVar()
        self.slice_n_tx = tk.IntVar(value=str(n_slices//2))
        self.slice_n_sg = tk.IntVar(value=str(n_slices//2))
        self.slice_n_co = tk.IntVar(value=str(n_slices//2))
        self.color_bar = tk.Scale(parent, label= "Saturation", orient='horizontal', to=99,
                                   variable=self.sat_percentage, command=self.controller.update_imgs)
        self.slice_bar_tx = tk.Scale(parent, orient='horizontal', to=n_slices-1,
                                   variable=self.slice_n_tx, command=self.controller.update_imgs)
        self.slice_bar_sg = tk.Scale(parent, orient='horizontal', to=n_slices-1,
                                   variable=self.slice_n_sg, command=self.controller.update_imgs)
        self.slice_bar_co = tk.Scale(parent, orient='horizontal', to=n_slices-1,
                                   variable=self.slice_n_co, command=self.controller.update_imgs)
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)
        parent.rowconfigure(3, weight=1)
        parent.columnconfigure(0, weight=1)
        self.color_bar.grid(row=0,column=0, sticky='nsew')
        self.slice_bar_tx.grid(row=1,column=0, sticky='nsew')
        self.slice_bar_co.grid(row=2,column=0, sticky='nsew')
        self.slice_bar_sg.grid(row=3,column=0, sticky='nsew')
        
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
        self.shx_frame = ttk.Frame(parent, height=int(round(rootHeight/2)),
                                    width=int(round(rootWidth/3)))
        self.hla_frame = ttk.Frame(parent, height=int(round(rootHeight/2)),
                                   width=int(round(rootWidth/3)))
        self.vla_frame = ttk.Frame(parent, height=int(round(rootHeight/2)),
                                   width=int(round(rootWidth/3)))
        #Transaxial view frame
        self.tax_frame.rowconfigure(0, weight=1)
        self.tax_frame.rowconfigure(1, weight=1)
        self.tax_frame.columnconfigure(0, weight=1)
        #Coronary view frame
        self.co_frame.rowconfigure(0, weight=1)
        self.co_frame.rowconfigure(1, weight=1)
        self.co_frame.columnconfigure(0, weight=1)
        #Saggital view frame
        self.sg_frame.rowconfigure(0, weight=1)
        self.sg_frame.rowconfigure(1, weight=1)
        self.sg_frame.columnconfigure(0, weight=1)
        #Short axis view frame
        self.shx_frame.rowconfigure(0, weight=1)
        self.shx_frame.rowconfigure(1, weight=1)
        self.shx_frame.columnconfigure(0, weight=1)
        #Horizontal long axis view frame
        self.hla_frame.rowconfigure(0, weight=1)
        self.hla_frame.rowconfigure(1, weight=1)
        self.hla_frame.columnconfigure(0, weight=1)
        #Vertical long axis view frame
        self.vla_frame.rowconfigure(0, weight=1)
        self.vla_frame.rowconfigure(1, weight=1)
        self.vla_frame.columnconfigure(0, weight=1)

        #Position frames
        self.tax_frame.grid(row=0, column=0, sticky='nsew')
        self.co_frame.grid(row=0, column=1, sticky='nsew')
        self.sg_frame.grid(row=0, column=2, sticky='nsew')
        self.shx_frame.grid(row=1, column=0, sticky='nsew')
        self.hla_frame.grid(row=1, column=1, sticky='nsew')
        self.vla_frame.grid(row=1, column=2, sticky='nsew')
        #Create labels
        self.tax_lbl = tk.Label(self.tax_frame, text="Transaxial", width=int(round(rootWidth/3)))
        self.co_lbl = tk.Label(self.co_frame, text="Coronal", width=int(round(rootWidth/3)))
        self.sg_lbl = tk.Label(self.sg_frame, text="Saggital", width=int(round(rootWidth/3)))
        self.shx_lbl = tk.Label(self.shx_frame, text="Short axis", width=int(round(rootWidth/3)))
        self.hla_lbl = tk.Label(self.hla_frame, text="HLA", width=int(round(rootWidth/3)))
        self.vla_lbl = tk.Label(self.vla_frame, text="VLA", width=int(round(rootWidth/3)))
        #Create images
        self.tax_img = tk.Canvas(self.tax_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        self.co_img = tk.Canvas(self.co_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        self.sg_img = tk.Canvas(self.sg_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        self.shx_img = tk.Canvas(self.shx_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        self.hla_img = tk.Canvas(self.hla_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        self.vla_img = tk.Canvas(self.vla_frame, width=int(round(rootWidth/3)),
                                  height=int(round(rootHeight/2)))
        #Position labels
        self.tax_lbl.grid(row=0,column=0)
        self.co_lbl.grid(row=0,column=0)
        self.sg_lbl.grid(row=0,column=0)
        self.shx_lbl.grid(row=0,column=0)
        self.hla_lbl.grid(row=0,column=0)
        self.vla_lbl.grid(row=0,column=0)
        #Posiiton images
        self.tax_img.grid(row=1, column=0, sticky='nsew')
        self.co_img.grid(row=1, column=0, sticky='nsew')
        self.sg_img.grid(row=1, column=0, sticky='nsew')
        self.shx_img.grid(row=1, column=0, sticky='nsew')
        self.hla_img.grid(row=1, column=0, sticky='nsew')
        self.vla_img.grid(row=1, column=0, sticky='nsew')

    def update_tax_img(self, img, eps=1e-3):
        w = self.tax_img.winfo_reqwidth()
        h = self.tax_img.winfo_reqheight()
        #Saturation
        new_sat_p = float(self.sat_percentage.get())/100.0
        sat_img = img.clip(max=img.max()*(1.0-new_sat_p))
        rgb_img= (plt.get_cmap('CMRmap')(sat_img/(sat_img.max()+eps))*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('ta_pic.png')
        self.tax_ph_image = tk.PhotoImage(file='./ta_pic.png', width=w, height=h)
        self.tax_img.create_image(0, 0, anchor=tk.NW, image=self.tax_ph_image)

    def update_co_img(self, img, eps=1e-3):
        w = self.tax_img.winfo_reqwidth()
        h = self.tax_img.winfo_reqheight()
        #Saturation
        new_sat_p = float(self.sat_percentage.get())/100.0
        sat_img = img.clip(max=img.max()*(1.0-new_sat_p))
        rgb_img= (plt.get_cmap('CMRmap')(sat_img/(sat_img.max()+eps))*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('co_pic.png')
        self.co_ph_image = tk.PhotoImage(file='./co_pic.png',width=w, height=h)
        self.co_img.create_image(0, 0, anchor=tk.NW, image=self.co_ph_image)

    def update_sg_img(self, img, eps=1e-3):
        w = self.tax_img.winfo_reqwidth()
        h = self.tax_img.winfo_reqheight()
        #Saturation
        new_sat_p = float(self.sat_percentage.get())/100.0
        sat_img = img.clip(max=img.max()*(1.0-new_sat_p))
        rgb_img= (plt.get_cmap('CMRmap')(sat_img/(sat_img.max()+eps))*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('sg_pic.png')
        self.sg_ph_image = tk.PhotoImage(file='./sg_pic.png',width=w, height=h)
        self.sg_img.create_image(0, 0, anchor=tk.NW, image=self.sg_ph_image)

    def update_shx_img(self, img, eps=1e-3):
        w = self.tax_img.winfo_reqwidth()
        h = self.tax_img.winfo_reqheight()
        #Saturation
        new_sat_p = float(self.sat_percentage.get())/100.0
        sat_img = img.clip(max=img.max()*(1.0-new_sat_p))
        rgb_img= (plt.get_cmap('CMRmap')(sat_img/(sat_img.max()+eps))*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('shx_pic.png')
        self.shx_ph_image = tk.PhotoImage(file='./shx_pic.png',width=w, height=h)
        self.shx_img.create_image(0, 0, anchor=tk.NW, image=self.shx_ph_image)
    
    def update_hla_img(self, img, eps=1e-3):
        w = self.tax_img.winfo_reqwidth()
        h = self.tax_img.winfo_reqheight()
        #Saturation
        new_sat_p = float(self.sat_percentage.get())/100.0
        sat_img = img.clip(max=img.max()*(1.0-new_sat_p))
        rgb_img= (plt.get_cmap('CMRmap')(sat_img/(sat_img.max()+eps))*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('hla_pic.png')
        self.hla_ph_image = tk.PhotoImage(file='./hla_pic.png',width=w, height=h)
        self.hla_img.create_image(0, 0, anchor=tk.NW, image=self.hla_ph_image)

    def update_vla_img(self, img, eps=1e-3):
        w = self.tax_img.winfo_reqwidth()
        h = self.tax_img.winfo_reqheight()
        #Saturation
        new_sat_p = float(self.sat_percentage.get())/100.0
        sat_img = img.clip(max=img.max()*(1.0-new_sat_p))
        rgb_img= (plt.get_cmap('CMRmap')(sat_img/(sat_img.max()+eps))*255).astype(np.uint8)
        pil_img = Image.fromarray(rgb_img, mode="RGBA").resize((w,h), Image.BICUBIC)
        pil_img.save('vla_pic.png')
        self.vla_ph_image = tk.PhotoImage(file='./vla_pic.png',width=w, height=h)
        self.vla_img.create_image(0, 0, anchor=tk.NW, image=self.vla_ph_image)

    def create_buttons(self, parent):
        self.prev_button = ttk.Button(parent, text="Previous study", command=self.controller.prev_study)
        self.next_button = ttk.Button(parent, text="Next study", command=self.controller.next_study)
        #Create radiobuttons for scoring
        self.score_label = tk.Label(parent, text="Would change reorientation:")
        self.r_buttons_list = []
        self.score_val = tk.IntVar()
        for i in range(1,6):
            self.r_buttons_list.append(ttk.Radiobutton(parent, text=SCORES[i-1],
                                        variable=self.score_val, value=i, command=self.set_score))
        #Position buttons
        self.prev_button.grid(row=0, column=0, sticky="nsew")
        self.next_button.grid(row=0, column=1, sticky="nsew")
        self.score_label.grid(row=0, column=2, sticky='nsew')
        for i in range(5):
            self.r_buttons_list[i].grid(row=0, column=3+i, sticky='nsew')
        #Next buton is disabled until scoring
        self.disable_next_button()

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

    def set_score(self):
        """
        Handle score radio button interaction
        :return:
        """
        self.enable_next_button()
        
    def reset_score(self):
        self.score_val.set(None)