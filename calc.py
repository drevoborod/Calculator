#!/usr/bin/env python3

import math
import tkinter as tk
import tkinter.font as fontconfig


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(width=0, height=0)
        self.title("Calculator")
        self.engine = Operations()
        self.indicator = tk.Label(self, relief='sunken', width=30, text=self.engine.digit, anchor='e', padx=10)
        font_config(self.indicator, size=20)
        self.indicator.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
        CalcButton(self, text="←", bold=True, command=(lambda: self.press_button("←"))).grid(row=0, column=7, padx=5, pady=5, sticky='news')
        for index, value in enumerate(("M", "MC", "MR", "M-", "M+")):
            CalcButton(self, text=value, bold=True, command=(lambda x=value: self.press_button(x))).grid(
                row=1, column=index, padx=5, pady=5, sticky='news')
        CalcButton(self, text="CE", bold=True, command=(lambda: self.press_button("CE"))).grid(row=1, column=6, padx=5, pady=5, sticky='news')
        CalcButton(self, text="C", bold=True, command=(lambda: self.press_button("C"))).grid(row=1, column=7, padx=5, pady=5, sticky='news')
        buttons_frame = tk.Frame(self)
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
        # Превращение списка списков в один список: [x for sublist in l for x in sublist]
        self.mainloop()

    def place_buttons(self, buttons, parent):
        r = 0
        for row in buttons:
            c = 0
            for button in row:
                CalcButton(parent, text=button, textsize=20, command=(lambda x=button: self.press_button(
                    x))).grid(row=r, column=c, sticky='news', padx=5, pady=5)
                c += 1
            r += 1

    def press_button(self, button):
        self.indicator.config(text=self.engine.button_press(button))


class CalcButton(tk.Button):
    def __init__(self, parent, textsize=15, bold=False, italic=False, **options):
        super().__init__(parent, **options)
        font_config(self, size=textsize, bold=bold, italic=italic)


class Operations:
    digit = ["0"]
    previous = 0
    operation = None
    memory = None

    def button_press(self, button):
        if len(self.digit) < 31:
            if button == ".":
                self.digit.append(button)
                res = self.digit[:-1]
            elif button in ("+", "-", "/", "•", "x^y", "%"):
                res = self.calculate(button)
            elif button == "√":
                self.digit = ["0"]
                self.previous = math.sqrt(self._digit_f())
                res = self.previous
            elif button == "=":
                res = self.calculate()
            elif button == "←":
                self._del()
                res = self.digit
            elif button == "M":
                self.memory = self._digit_f()
                res = self.digit
            elif button == "MC":
                self.memory = None
                res = self.digit
            elif button == "MR":
                self.digit = list(str(self.memory))
                res = self.digit
            elif button == "M+" or button == "M-":
                self.calculate_memory(button[-1])
                res = self.digit
            elif button == "CE":
                self.digit = ["0"]
                res = self.digit
            elif button == "C":
                self.digit = ["0"]
                self.previous = 0
                self.operation = None
                res = self.digit
            elif button in range(0, 10):
                if self.digit[0] == "0" and len(self.digit) == 1:
                    self.digit.pop(0)
                self.digit.append(str(button))
                res = self.digit
        else:
            res = self.digit
        return "".join(res)

    def calculate(self, operation=None):
        if self.operation == "%":
            res = self.calculate_percent()
        elif self.operation:
            exec("self.previous = {0} {1} {2}".format(self.previous, self.operation, self._digit_f()))
            res = list(str(self.previous))
        else:
            self.previous = self._digit_f()
            res = self.digit
        self.digit = ["0"]
        if operation == "•":
            self.operation = "*"
        elif operation == "x^y":
            self.operation = "^"
        else:
            self.operation = operation
        return res

    def calculate_percent(self): pass

    def calculate_memory(self, operation):
        if self.memory:
            exec("self.memory = {0} {1} {2}".format(self.memory, operation, self._digit_f()))

    def _del(self):
        if len(self.digit) > 0:
            self.digit.pop()
            if len(self.digit) == 0:
                self.digit = ["0"]
            elif self.digit[-1] == ".":
                self.digit.pop()

    def _digit_f(self):
        return float("".join(self.digit))


def font_config(unit, size=9, bold=False, italic=False):
    """Change font of a provided unit."""
    fontname = fontconfig.Font(font=unit['font']).actual()['family']
    font_params = [fontname, size]
    if bold:
        font_params.append("bold")
    if italic:
        font_params.append("italic")
    unit.config(font=tuple(font_params))


if __name__ == "__main__":
    Main()