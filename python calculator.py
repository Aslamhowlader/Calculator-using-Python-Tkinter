import tkinter as tk
from tkinter import font
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("পাইথন ক্যালকুলেটর")
        self.root.geometry("400x600")
        self.root.configure(bg='#2e2e2e')
        
        # ভেরিয়েবল ডিক্লেয়ারেশন
        self.current_input = ""
        self.result = ""
        self.operator = ""
        self.waiting_for_operand = False
        
        # ফন্ট সেটিংস
        self.display_font = font.Font(family='Arial', size=24, weight='bold')
        self.button_font = font.Font(family='Arial', size=16, weight='bold')
        
        # GUI তৈরি
        self.create_widgets()
        
    def create_widgets(self):
        # ডিসপ্লে এলাকা তৈরি
        self.display_frame = tk.Frame(self.root, bg='#2e2e2e', height=100)
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=(20, 10))
        
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            self.display_frame, 
            textvariable=self.display_var, 
            font=self.display_font,
            anchor='e',
            bg='#1a1a1a',
            fg='#ffffff',
            padx=20,
            pady=20
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # বাটন ফ্রেম তৈরি
        self.buttons_frame = tk.Frame(self.root, bg='#2e2e2e')
        self.buttons_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # বাটন লেআউট
        buttons = [
            ('C', '%', '←', '÷'),
            ('7', '8', '9', '×'),
            ('4', '5', '6', '-'),
            ('1', '2', '3', '+'),
            ('±', '0', '.', '=')
        ]
        
        # বাটন তৈরি এবং গ্রিডে স্থাপন
        for row_idx, row in enumerate(buttons):
            self.buttons_frame.rowconfigure(row_idx, weight=1)
            for col_idx, text in enumerate(row):
                self.buttons_frame.columnconfigure(col_idx, weight=1)
                
                # বিশেষ বাটনের জন্য রং আলাদা করা
                if text in ['C', '←', '±']:
                    bg_color = '#616161'  # ধূসর
                    fg_color = '#ffffff'
                elif text in ['÷', '×', '-', '+', '=']:
                    bg_color = '#ff9500'  # কমলা
                    fg_color = '#ffffff'
                elif text == '%':
                    bg_color = '#616161'  # ধূসর
                    fg_color = '#ffffff'
                else:
                    bg_color = '#a5a5a5'  # হালকা ধূসর
                    fg_color = '#000000'
                
                # বাটন তৈরি
                button = tk.Button(
                    self.buttons_frame,
                    text=text,
                    font=self.button_font,
                    bg=bg_color,
                    fg=fg_color,
                    activebackground='#b3b3b3' if bg_color == '#a5a5a5' else '#8a8a8a' if bg_color == '#616161' else '#e68900',
                    activeforeground=fg_color,
                    borderwidth=0,
                    relief='flat',
                    command=lambda t=text: self.button_click(t)
                )
                button.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky='nsew')
                
                # বাটনের উপর মাউস হোভার ইফেক্ট
                button.bind("<Enter>", lambda e, b=button: self.on_enter(e, b))
                button.bind("<Leave>", lambda e, b=button: self.on_leave(e, b))
    
    def on_enter(self, event, button):
        """মাউস হোভার করার সময় বাটনের রং পরিবর্তন"""
        current_bg = button.cget('bg')
        if current_bg == '#a5a5a5':
            button.config(bg='#b8b8b8')
        elif current_bg == '#616161':
            button.config(bg='#707070')
        elif current_bg == '#ff9500':
            button.config(bg='#ffad33')
    
    def on_leave(self, event, button):
        """মাউস সরিয়ে নেওয়ার পর বাটনের রং পূর্বাবস্থায় ফেরত"""
        current_text = button.cget('text')
        if current_text in ['C', '←', '±']:
            button.config(bg='#616161')
        elif current_text in ['÷', '×', '-', '+', '=']:
            button.config(bg='#ff9500')
        elif current_text == '%':
            button.config(bg='#616161')
        else:
            button.config(bg='#a5a5a5')
    
    def button_click(self, value):
        """বাটন ক্লিক হ্যান্ডলার"""
        if value == 'C':
            self.clear_all()
        elif value == '←':
            self.backspace()
        elif value == '±':
            self.toggle_sign()
        elif value == '%':
            self.percentage()
        elif value == '.':
            self.add_decimal()
        elif value == '=':
            self.calculate()
        elif value in ['+', '-', '×', '÷']:
            self.set_operator(value)
        else:  # সংখ্যা
            self.add_digit(value)
    
    def add_digit(self, digit):
        """সংখ্যা যোগ করা"""
        if self.waiting_for_operand:
            self.current_input = ""
            self.waiting_for_operand = False
        
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.update_display()
    
    def add_decimal(self):
        """দশমিক যোগ করা"""
        if self.waiting_for_operand:
            self.current_input = "0."
            self.waiting_for_operand = False
        elif "." not in self.current_input:
            if self.current_input == "":
                self.current_input = "0."
            else:
                self.current_input += "."
        
        self.update_display()
    
    def set_operator(self, op):
        """অপারেটর সেট করা"""
        if self.current_input:
            if self.result and not self.waiting_for_operand:
                self.calculate()
            
            self.result = self.current_input
            self.current_input = ""
        
        # অপারেটর ম্যাপিং (ডিসপ্লেতে দেখানোর জন্য)
        op_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}
        self.operator = op_map[op]
        self.waiting_for_operand = True
        
        # ডিসপ্লেতে অপারেটর দেখানো
        display_op = op
        if self.result:
            self.display_var.set(f"{self.result} {display_op}")
        else:
            self.display_var.set(display_op)
    
    def calculate(self):
        """গণনা সম্পন্ন করা"""
        if not self.result or not self.current_input or not self.operator:
            return
        
        try:
            # স্ট্রিংকে সংখ্যায় রূপান্তর
            num1 = float(self.result)
            num2 = float(self.current_input)
            
            # অপারেটর অনুযায়ী গণনা
            if self.operator == '+':
                result = num1 + num2
            elif self.operator == '-':
                result = num1 - num2
            elif self.operator == '*':
                result = num1 * num2
            elif self.operator == '/':
                if num2 == 0:
                    self.display_var.set("অসীম")
                    self.current_input = ""
                    self.result = ""
                    self.operator = ""
                    return
                result = num1 / num2
            
            # ফলাফল সেট করা
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10)).rstrip('0').rstrip('.')
            
            self.result = ""
            self.operator = ""
            self.waiting_for_operand = True
            self.update_display()
            
        except Exception as e:
            self.display_var.set("ত্রুটি")
            self.current_input = ""
            self.result = ""
            self.operator = ""
    
    def clear_all(self):
        """সব ডেটা ক্লিয়ার করা"""
        self.current_input = ""
        self.result = ""
        self.operator = ""
        self.waiting_for_operand = False
        self.display_var.set("0")
    
    def backspace(self):
        """একটি সংখ্যা মুছে ফেলা"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
            self.update_display()
    
    def toggle_sign(self):
        """ধনাত্মক/ঋণাত্মক চিহ্ন পরিবর্তন"""
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def percentage(self):
        """শতাংশ গণনা"""
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                if value.is_integer():
                    self.current_input = str(int(value))
                else:
                    self.current_input = str(value)
                self.update_display()
            except:
                self.display_var.set("ত্রুটি")
                self.current_input = ""
    
    def update_display(self):
        """ডিসপ্লে আপডেট করা"""
        if self.current_input:
            # দীর্ঘ সংখ্যা হলে ফন্ট সাইজ কমিয়ে দেখানো
            if len(self.current_input) > 15:
                self.display.config(font=('Arial', 18, 'bold'))
            else:
                self.display.config(font=self.display_font)
            
            self.display_var.set(self.current_input)
        else:
            self.display.config(font=self.display_font)
            if self.result and self.operator:
                # অপারেটর ম্যাপিং (ডিসপ্লেতে দেখানোর জন্য)
                op_map = {'+': '+', '-': '-', '*': '×', '/': '÷'}
                display_op = op_map.get(self.operator, self.operator)
                self.display_var.set(f"{self.result} {display_op}")
            elif self.result:
                self.display_var.set(self.result)
            else:
                self.display_var.set("0")

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()