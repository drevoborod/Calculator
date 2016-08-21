from tkinter import *

class BigFrame(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

class IndicatorFrame(BigFrame):
    def __init__(self):
        BigFrame.__init__(self)
        self.indicatortext = 0
        self.indicator = Label(self, text=self.indicatortext, justify=RIGHT)
        self.indicator.pack(side=TOP)
        self.changebutton = Button(self, text="Change mode", command=self.change_window)
        self.changebutton.pack()
        self.window_id = 2
        self.button_window = CalcButtonsFrame(self)

    def change_window(self):
        self.button_window.destroy()
        if self.window_id == 1:
            self.button_window = CalcButtonsFrame(self)
            self.window_id = 2
        elif self.window_id == 2:
            self.button_window = OtherButtonsFrame(self)
            self.window_id = 1


class CalcButtonsFrame(BigFrame):
    def __init__(self, parent):
        BigFrame.__init__(self, parent=parent)
        self.parent = parent
        self.change_indicator_button = Button(self, text=1, command=self.change_indicator)
        self.change_indicator_button.pack(side=BOTTOM)

    def change_indicator(self):
        self.parent.indicator.config(text="Window 1")


class OtherButtonsFrame(BigFrame):
    def __init__(self, parent):
        BigFrame.__init__(self, parent=parent)
        self.parent = parent
        self.change_indicator_button = Button(self, text=2, command=self.change_indicator)
        self.change_indicator_button.pack(side=BOTTOM)

    def change_indicator(self):
        self.parent.indicator.config(text="Window 2")


run = IndicatorFrame()
run.mainloop()