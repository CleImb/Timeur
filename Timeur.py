#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Coded by Clément Imbert : clement.imbert@outlook.com

from Tkinter import *
from time import *

class Timeur():
    """
    After demanding to user to submit a time, display a timeur 
    at the bottom right to the screen. There is pause button. 
    Remaining and pause (in progress and accumulated) times are shown.
    """

    def __init__(self):
        """ Display entry zone where the user can submit time """
        self.root = Tk()
        self.root.title("Timeur")
        # window is on top of all others
        self.root.attributes('-topmost', 1)
        # canvas for time choice
        self.canvas = Canvas()
        self.canvas.pack(ipady =4, ipadx =8)
        # user enter time for timeur
        Label(self.canvas, text ="Temps en seconde,\néquations acceptées").pack(pady =4)
        self.user_entry = StringVar()
        entry =Entry(self.canvas, textvariable = self.user_entry, width =16)
        entry.bind("<Return>", self.check_error)
        entry.bind("<KP_Enter>", self.check_error)
        entry.focus_set()
        entry.pack()

        self.root.mainloop()

    def check_error(self, event):
        """ Test text entry, compile equation """
        try:
            self.temps_program = eval(self.user_entry.get())
        except:
            return
        self.display_timer()

    def display_timer(self):
        """ Display timeur with choosen time and pause button """
        # destroy canvas for time choice
        self.canvas.destroy()
        # display time
        self.frame_temps =Frame()
        self.frame_temps.pack()
        self.label =Label(self.frame_temps, text ="", font=("Helvetica", 18))
        self.label.pack()
        # button pause
        self.pause =False
        self.pause_bouton = Button(text ="Pause", command=self.stop_clock)
        self.pause_bouton.pack(fill =X)
        # time when timeur starts
        self.debut =time()
        # init temps pause cumu
        self.pause_cumu =0
        # go function
        self.update_clock()

    def update_clock(self):
        """ Manage times to display according to pause """

        if self.pause ==False:      # pause is off
            # calcul temps restant
            temps_ecoule =time() -self.debut
            temps_restant =self.temps_program -temps_ecoule
            # display temps restant
            temps_affiche =strftime("%H:%M:%S", gmtime(temps_restant))
            self.label.configure(text =temps_affiche)

        elif self.pause ==True:     # pause is on
            # calcul temps pause
            self.temps_pause =time() -self.debut_pause
            # calcul temps pause cumulé
            self.temps_pause_cumu =self.pause_cumu +self.temps_pause
            # display temps pause
            self.temps_pause_affiche =strftime("%H:%M:%S", gmtime(self.temps_pause))
            self.label_pause.configure(text =self.temps_pause_affiche)
            # display temps pause cumulé
            self.temps_pause_cumu_affiche =strftime("%H:%M:%S", gmtime(self.temps_pause_cumu))
            self.label_pause_cumu.configure(text =self.temps_pause_cumu_affiche)
        
        # places the window at the bottom right
        self.location_window()
        # refresh all 0,1 secondes
        self.root.after(100, self.update_clock)

    def stop_clock(self):
        """ Actions when pause button is pressed """

        if self.pause ==False:      # pause on
            self.pause =True
            # time when pause begin
            self.debut_pause =time()
            # change time color and button text
            self.label.configure(fg ="red")
            self.pause_bouton.configure(text ="Reprendre")
            # frame displaying time pause
            self.frame_pause =Frame(self.frame_temps)
            self.frame_pause.pack()
            # labels displaying time pause
            Label(self.frame_pause, text ="pause:").grid(row =0, column =0)
            self.label_pause =Label(self.frame_pause, text ="")
            self.label_pause.grid(row =0, column =1)
            # labels displaying time pause cumulé
            Label(self.frame_pause, text ="cumulé:").grid(row =1, column =0)
            self.label_pause_cumu =Label(self.frame_pause, text ="")
            self.label_pause_cumu.grid(row =1, column =1)

        else:                       # pause off
            self.pause =False
            # add time pause to time pause cumulé
            self.pause_cumu =self.pause_cumu +self.temps_pause
            # add time pause to time debut
            self.debut =self.debut +self.temps_pause
            # change time color and button text
            self.label.configure(fg ="black")
            self.pause_bouton.configure(text ="Pause")
            # destroy frame displaying time pause
            self.frame_pause.destroy()

    def location_window(self):
        """ Places the window at the bottom right """
        x =self.root.winfo_screenwidth() -self.root.winfo_width()
        y =self.root.winfo_screenheight() -self.root.winfo_height() -25
        self.root.geometry('+%d+%d' %(x, y))

app =Timeur()