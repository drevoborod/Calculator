#!/usr/bin/env python3

import math
import tkinter as tk
import tkinter.font as fontconfig
from tkinter.messagebox import showinfo


class Main(tk.Tk):
    """Calculator GUI."""
    def __init__(self):
        super().__init__()
        self.resizable(width=0, height=0)
        self.title("Calculator")
        # Class containing all calculator logic:
        self.engine = Operations()
        # Additional Indicator:
        self.second_indicator = tk.Text(self, width=1, height=2, state='disabled', wrap='char')
        font_config(self.second_indicator, size=12, bold=True)
        self.second_indicator.grid(row=0, column=0, pady=5, sticky='e')
        # Main Indicator:
        self.indicator = tk.Label(self, relief='sunken', width=30, text=self.engine.digit, anchor='e', padx=10)
        font_config(self.indicator, size=20)
        self.indicator.grid(row=0, column=1, columnspan=7, padx=5, pady=5)
        # Different buttons:
        CalcButton(self, text="←", bold=True, command=(lambda: self.press_button("←"))).grid(row=0, column=8, padx=5, pady=5, sticky='news')
        for index, value in enumerate(("M", "MC", "MR", "M-", "M+")):
            CalcButton(self, text=value, bold=True, command=(lambda x=value: self.memory_button(x))).grid(
                row=1, column=index, padx=5, pady=5, sticky='news')
        CalcButton(self, text="CE", bold=True, command=(lambda: self.press_button("CE"))).grid(row=1, column=7, padx=5, pady=5, sticky='news')
        CalcButton(self, text="C", bold=True, command=(lambda: self.press_button("C"))).grid(row=1, column=8, padx=5, pady=5, sticky='news')
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=2, column=0, columnspan=9, pady=10)
        self.grid_columnconfigure('all', minsize=80)
        numbuttons_frame = tk.Frame(buttons_frame)
        funcbuttons_frame = tk.Frame(buttons_frame)
        numbuttons_frame.grid(row=0, column=0, padx=5, sticky='w')
        funcbuttons_frame.grid(row=0, column=1, padx=5, sticky='e')
        # Buttons with numbers:
        number_buttons = ([*range(7, 10)], [*range(4, 7)], [*range(1, 4)], [".", 0, "±"])
        # Buttons for mathematical operations:
        oper_buttons = (["÷", "√"], ["×", "x^y"], ["-", "%"], ["+", "="])
        self.place_buttons(number_buttons, numbuttons_frame)
        self.place_buttons(oper_buttons, funcbuttons_frame)
        numbuttons_frame.grid_columnconfigure('all', minsize=150)
        funcbuttons_frame.grid_columnconfigure('all', minsize=90)
        # Превращение списка списков в один список: [x for sublist in l for x in sublist]
        self.mainloop()

    def place_buttons(self, buttons, parent):
        """Create a grid of buttons in provided container.
        buttons should be a tuple or list of lists."""
        r = 0
        for row in buttons:
            c = 0
            for button in row:
                CalcButton(parent, text=button, textsize=20, command=(lambda x=button: self.press_button(
                    x))).grid(row=r, column=c, sticky='news', padx=5, pady=5)
                c += 1
            r += 1

    def press_button(self, button):
        self.engine.button_press(button)
        self.change_indicator()

    def memory_button(self, button):
        self.engine.memory_actions(button)
        self.change_indicator()

    def change_indicator(self):
        self.indicator.config(text="".join(self.engine.digit))
        self.second_indicator_change()

    def second_indicator_change(self):
        self.second_indicator.config(state="normal")
        self.second_indicator.delete(1.0, 'end')
        if self.engine.memory:
            self.second_indicator.insert('end', "M")
        if self.engine.minus:
            self.second_indicator.insert('end', "-" if self.engine.memory else "\n-")
        self.second_indicator.config(state="disabled")


class CalcButton(tk.Button):
    def __init__(self, parent, textsize=15, bold=False, italic=False, **options):
        super().__init__(parent, **options)
        font_config(self, size=textsize, bold=bold, italic=italic)


class Operations:
    """Calculator engine."""
    digit = ["0"]       # Indicator contents.
    previous = 0        # Previous value for mathematical operation.
    operation = None    # Mathematical operation sign.
    memory = None       # Contents of calculator's memory.
    minus = False       # Is number negative.
    prev_button = None  # Previous pressed button.
    default = False     # Should indicator contents be set to default value.
    funcbuttons = "+", "-", "÷", "×", "x^y", "%"

    def button_press(self, button):
        """Main entry point for every button press."""
        #self._debug(button)
        if self.prev_button in (self.funcbuttons + ("√", "=")):
            if button in (self.funcbuttons + ("√", "=")):
                self.default = False
            else:
                self.default = True
        if self.default:
            self.digit = ["0"]
            self.default = False
        if len(self.digit) < 31:
            if button == ".":
                if "." not in self.digit:
                    self.digit.append(button)
            elif button in self.funcbuttons:
                self.digit = self.calculate(button)
            elif button == "√":
                if not self.minus:
                    self.previous = math.sqrt(self._digit_f())
                    self.default = True
                    self.digit = list(str(self.previous))
                else:
                    showinfo("Error", "Cannot calculate square root from a negative number.")
            elif button == "=":
                self.digit = self.calculate()
            elif button == "←":
                self._del()
            elif button == "CE":
                self.minus = False
                self.digit = ["0"]
            elif button == "C":
                self.previous = 0
                self.operation = None
                self.minus = False
                self.digit = ["0"]
            elif button == "±":
                if self.minus:
                    self.minus = False
                else:
                    self.minus = True
            elif button in range(0, 10):
                if self.digit[0] == "0" and len(self.digit) == 1:
                    self.digit.pop(0)
                self.digit.append(str(button))
        self.prev_button = button

    def memory_actions(self, button):
        if button == "M":
            self.memory = self._digit_f()
        elif button == "MC":
            self.memory = None
        elif button == "MR":
            if self.memory:
                self.minus = False
                self.digit = self._set_minus(list(str(self.memory)))
                self.digit = self._remove_tail(self.digit)
        elif button == "M+" or button == "M-":
            self.calculate_memory(button[-1])
        if self.prev_button in (self.funcbuttons + ("√", "=")):
            self.default = True

    def calculate(self, operation=None):
        """All mathematical operations."""
        res = self.digit
        if self.operation == "%":
            res = self.calculate_percent()
        elif self.operation:
            if self.prev_button not in self.funcbuttons:
                try:
                    if self.operation == "^":
                        exec("self.previous = {0} {1} {3}{2}".format(int(self.previous), self.operation, int(self._digit_f()),
                                                                     "-" if self.minus else ""))
                    else:
                        exec("self.previous = {0} {1} {3}{2}".format(self.previous, self.operation, self._digit_f(),
                                                                     "-" if self.minus else ""))
                except ZeroDivisionError:
                    showinfo("Error", "Division by zero.")
                    self.default = True
                else:
                    res = list(str(self.previous))
        else:
            self.previous = self._digit_f()
        self._set_operation(operation)
        res = self._set_minus(res)
        return self._remove_tail(res)

    def calculate_percent(self):
        return list(str(self.previous / 100 * self._digit_f()))

    def calculate_memory(self, operation):
        if self.memory:
            exec("self.memory = {0} {1} {2}".format(self.memory, operation, self._digit_f()))

    def _set_operation(self, button):
        """Set contents of 'operation' class variable."""
        if button == "×":
            self.operation = "*"
        elif button == "x^y":
            self.operation = "^"
        elif button == "÷":
            self.operation = "/"
        else:
            self.operation = button

    def _set_minus(self, value):
        if value[0] == "-":
            self.minus = True
            value.pop(0)
        return value

    def _del(self):
        """Remove one char from indicator."""
        if len(self.digit) > 0:
            self.digit.pop()
            if len(self.digit) == 0:
                self.digit = ["0"]
            elif self.digit[-1] == ".":
                self.digit.pop()

    def _remove_tail(self, value):
        if len(value) >= 3 and value[-1] == "0" and value[-2] == ".":
            value = value[:-2]
        return value

    def _digit_f(self):
        """Translate indicator contents to float."""
        res = self.digit[:]
        if self.minus:
            res.insert(0, "-")
        return float("".join(res))

    def _debug(self, button=None):
        print("\n")
        if button:
            print("current button:", button)
        print("digit:", self.digit)
        print("previous:", self.previous)
        print("operation:", self.operation)
        print("memory", self.memory)
        print("minus:", self.minus)
        print("prev_button:", self.prev_button)


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

# ToDo: убрать излишнюю точность вычислений (0.2 * 0.2).
