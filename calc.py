#!/usr/bin/env python3

import tkinter as tk
import tkinter.font as fontconfig


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(width=0, height=0)
        self.title("Calculator")
        self.digit = []
        self.engine = Operations(self.digit)
        self.indicator = tk.Label(self, relief='sunken', width=30, text=0, anchor='e', padx=10)
        font_config(self.indicator, size=20)
        del_button = CalcButton(self, text="←", bold=True)
        m_button = CalcButton(self, text="M", bold=True)
        mc_button = CalcButton(self, text="MC", bold=True)
        mr_button = CalcButton(self, text="MR", bold=True)
        mplus_button = CalcButton(self, text="M-", bold=True)
        mminus_button = CalcButton(self, text="M+", bold=True)
        ce_button = CalcButton(self, text="CE", bold=True)
        c_button = CalcButton(self, text="C", bold=True)
        buttons_frame = tk.Frame(self)
        self.indicator.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
        del_button.grid(row=0, column=7, padx=5, pady=5, sticky='news')
        m_button.grid(row=1, column=0, padx=5, pady=5, sticky='news')
        mc_button.grid(row=1, column=1, padx=5, pady=5, sticky='news')
        mr_button.grid(row=1, column=2, padx=5, pady=5, sticky='news')
        mplus_button.grid(row=1, column=3, padx=5, pady=5, sticky='news')
        mminus_button.grid(row=1, column=4, padx=5, pady=5, sticky='news')
        ce_button.grid(row=1, column=6, padx=5, pady=5, sticky='news')
        c_button.grid(row=1, column=7, padx=5, pady=5, sticky='news')
        buttons_frame.grid(row=2, column=0, columnspan=8, pady=10)
        self.grid_columnconfigure('all', minsize=70)
        numbuttons_frame = tk.Frame(buttons_frame)
        funcbuttons_frame = tk.Frame(buttons_frame)
        numbuttons_frame.grid(row=0, column=0, padx=5)
        funcbuttons_frame.grid(row=0, column=1, padx=5)
        number_buttons = ([*range(7, 10)], [*range(4, 7)], [*range(1, 4)], [".", 0, "±"])
        oper_buttons = (["/", "√"], ["•", "x^y"], ["-", "%"], ["+", "="])
        self.place_buttons(number_buttons, numbuttons_frame)
        self.place_buttons(oper_buttons, funcbuttons_frame)
        numbuttons_frame.grid_columnconfigure('all', minsize=130)
        funcbuttons_frame.grid_columnconfigure('all', minsize=90)
        self.mainloop()

    def place_buttons(self, buttons, parent):
        r = 0
        for row in buttons:
            c = 0
            for button in row:
                CalcButton(parent, text=button, textsize=20, command=(lambda x=button: self.engine.button_press(
                    x))).grid(row=r, column=c, sticky='news', padx=5, pady=5)
                c += 1
            r += 1


class CalcButton(tk.Button):
    def __init__(self, parent, textsize=15, bold=False, italic=False, **options):
        super().__init__(parent, **options)
        font_config(self, size=textsize, bold=bold, italic=italic)


class Operations:
    def __init__(self, digit):
        self.digit = digit

    def button_press(self, button):
        print(button)


def font_config(unit, size=9, bold=False, italic=False):
    """Font size of a given unit change."""
    fontname = fontconfig.Font(font=unit['font']).actual()['family']
    font_params = [fontname, size]
    if bold:
        font_params.append("bold")
    if italic:
        font_params.append("italic")
    unit.config(font=tuple(font_params))


if __name__ == "__main__":
    Main()