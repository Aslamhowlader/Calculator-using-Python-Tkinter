import tkinter as tk
from tkinter import font, messagebox
import math
import json
import os
from datetime import datetime

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator - Python")
        self.root.geometry("500x700")
        self.root.configure(bg='#2e2e2e')
        
        # Theme settings
        self.dark_mode = True
        self.current_theme = {
            'bg': '#2e2e2e',
            'fg': '#ffffff',
            'display_bg': '#1a1a1a',
            'button_bg': '#a5a5a5',
            'button_fg': '#000000',
            'operator_bg': '#ff9500',
            'special_bg': '#616161'
        }
        
        # Variable declaration
        self.current_input = ""
        self.result = ""
        self.operator = ""
        self.waiting_for_operand = False
        self.memory = 0
        self.history = []
        
        # Font settings
        self.display_font = font.Font(family='Arial', size=24, weight='bold')
        self.button_font = font.Font(family='Arial', size=14, weight='bold')
        self.small_font = font.Font(family='Arial', size=10)
        
        # Keyboard shortcuts setup
        self.setup_keyboard_shortcuts()
        
        # Load history file
        self.load_history()
        
        # Create GUI
        self.create_widgets()
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Key>', self.key_pressed)
        
    def key_pressed(self, event):
        """Keyboard key press handler"""
        key = event.char
        keysym = event.keysym
        
        if key in '0123456789':
            self.add_digit(key)
        elif key == '.':
            self.add_decimal()
        elif key in '+-*/':
            op_map = {'+': '+', '-': '-', '*': '×', '/': '÷'}
            self.set_operator(op_map.get(key, key))
        elif key == '=' or key == '\r':  # Enter key
            self.calculate()
        elif key == '\x08':  # Backspace key
            self.backspace()
        elif key == 'c' or key == 'C':
            self.clear_all()
        elif key == 'm':
            if event.state & 0x4:  # Ctrl+M
                self.memory_store()
            elif event.state & 0x1:  # Shift+M
                self.memory_recall()
        elif keysym == 'Escape':
            self.clear_all()
    
    def create_widgets(self):
        # Title bar
        title_frame = tk.Frame(self.root, bg='#1a1a1a', height=40)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Advanced Calculator",
            font=('Arial', 14, 'bold'),
            bg='#1a1a1a',
            fg='#ff9500'
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Theme toggle button
        theme_btn = tk.Button(
            title_frame,
            text="☀️" if self.dark_mode else "🌙",
            font=('Arial', 12),
            bg='#1a1a1a',
            fg='#ffffff',
            borderwidth=0,
            command=self.toggle_theme
        )
        theme_btn.pack(side=tk.RIGHT, padx=20)
        
        # Memory indicator
        memory_frame = tk.Frame(self.root, bg=self.current_theme['bg'], height=30)
        memory_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))
        
        self.memory_label = tk.Label(
            memory_frame,
            text=f"Memory: {self.memory}",
            font=self.small_font,
            bg=self.current_theme['bg'],
            fg='#ff9500'
        )
        self.memory_label.pack(side=tk.LEFT)
        
        # Display area
        self.display_frame = tk.Frame(self.root, bg=self.current_theme['bg'], height=100)
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=(0, 10))
        
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            self.display_frame,
            textvariable=self.display_var,
            font=self.display_font,
            anchor='e',
            bg=self.current_theme['display_bg'],
            fg=self.current_theme['fg'],
            padx=20,
            pady=20,
            relief='sunken',
            borderwidth=2
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Memory buttons frame
        memory_btn_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        memory_btn_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))
        
        memory_buttons = [
            ('MC', self.memory_clear),
            ('MR', self.memory_recall),
            ('M+', self.memory_add),
            ('M-', self.memory_subtract),
            ('MS', self.memory_store)
        ]
        
        for text, command in memory_buttons:
            btn = tk.Button(
                memory_btn_frame,
                text=text,
                font=self.button_font,
                bg=self.current_theme['special_bg'],
                fg=self.current_theme['fg'],
                activebackground='#8a8a8a',
                borderwidth=0,
                relief='raised',
                command=command
            )
            btn.pack(side=tk.LEFT, padx=2, ipadx=10, ipady=5)
        
        # Scientific buttons frame
        sci_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        sci_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))
        
        sci_buttons = [
            ('sin', self.sine), ('cos', self.cosine), ('tan', self.tangent),
            ('log', self.logarithm), ('√', self.square_root), ('x²', self.square),
            ('π', self.pi), ('e', self.euler), ('x!', self.factorial)
        ]
        
        for i in range(0, len(sci_buttons), 3):
            row_frame = tk.Frame(sci_frame, bg=self.current_theme['bg'])
            row_frame.pack(fill=tk.X, pady=2)
            
            for j in range(3):
                if i + j < len(sci_buttons):
                    text, command = sci_buttons[i + j]
                    btn = tk.Button(
                        row_frame,
                        text=text,
                        font=self.button_font,
                        bg=self.current_theme['special_bg'],
                        fg=self.current_theme['fg'],
                        activebackground='#8a8a8a',
                        borderwidth=0,
                        relief='raised',
                        command=command
                    )
                    btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X, ipady=5)
        
        # Main buttons frame
        self.buttons_frame = tk.Frame(self.root, bg=self.current_theme['bg'])
        self.buttons_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button layout
        buttons = [
            ('(', ')', '%', '÷', 'C'),
            ('7', '8', '9', '×', '←'),
            ('4', '5', '6', '-', '1/x'),
            ('1', '2', '3', '+', '±'),
            ('0', '.', '=', '√', 'H')  # H for History
        ]
        
        # Create buttons and place in grid
        for row_idx, row in enumerate(buttons):
            self.buttons_frame.rowconfigure(row_idx, weight=1)
            for col_idx, text in enumerate(row):
                self.buttons_frame.columnconfigure(col_idx, weight=1)
                
                # Color coding for special buttons
                if text in ['C', '←', '±', '(', ')', '1/x', 'H']:
                    bg_color = self.current_theme['special_bg']
                    fg_color = self.current_theme['fg']
                elif text in ['÷', '×', '-', '+', '=']:
                    bg_color = self.current_theme['operator_bg']
                    fg_color = self.current_theme['fg']
                elif text == '%':
                    bg_color = self.current_theme['special_bg']
                    fg_color = self.current_theme['fg']
                else:
                    bg_color = self.current_theme['button_bg']
                    fg_color = '#000000'
                
                # Create button
                button = tk.Button(
                    self.buttons_frame,
                    text=text,
                    font=self.button_font,
                    bg=bg_color,
                    fg=fg_color,
                    activebackground='#b3b3b3' if bg_color == self.current_theme['button_bg'] else '#8a8a8a' if bg_color == self.current_theme['special_bg'] else '#e68900',
                    activeforeground=fg_color,
                    borderwidth=0,
                    relief='flat',
                    command=lambda t=text: self.button_click(t)
                )
                button.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky='nsew')
    
    def button_click(self, value):
        """Button click handler"""
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
        elif value in ['(', ')']:
            self.add_parenthesis(value)
        elif value == '1/x':
            self.reciprocal()
        elif value == 'H':
            self.show_history()
        else:  # Numbers
            self.add_digit(value)
    
    def add_digit(self, digit):
        """Add digit to input"""
        if self.waiting_for_operand:
            self.current_input = ""
            self.waiting_for_operand = False
        
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.update_display()
    
    def add_decimal(self):
        """Add decimal point"""
        if self.waiting_for_operand:
            self.current_input = "0."
            self.waiting_for_operand = False
        elif "." not in self.current_input:
            if self.current_input == "":
                self.current_input = "0."
            else:
                self.current_input += "."
        
        self.update_display()
    
    def add_parenthesis(self, paren):
        """Add parenthesis"""
        if self.waiting_for_operand:
            self.current_input = ""
            self.waiting_for_operand = False
        
        self.current_input += paren
        self.update_display()
    
    def set_operator(self, op):
        """Set operator"""
        if self.current_input:
            if self.result and not self.waiting_for_operand:
                self.calculate()
            
            self.result = self.current_input
            self.current_input = ""
        
        # Operator mapping (for display)
        op_map = {'+': '+', '-': '-', '×': '*', '÷': '/'}
        self.operator = op_map[op]
        self.waiting_for_operand = True
        
        # Display operator
        display_op = op
        if self.result:
            self.display_var.set(f"{self.result} {display_op}")
        else:
            self.display_var.set(display_op)
    
    def calculate(self):
        """Perform calculation"""
        if not self.result or not self.current_input or not self.operator:
            return
        
        try:
            # Convert string to number
            num1 = float(self.result)
            num2 = float(self.current_input)
            
            # Save expression for history
            expression = f"{self.result} {self.operator} {self.current_input}"
            
            # Perform operation based on operator
            if self.operator == '+':
                result = num1 + num2
            elif self.operator == '-':
                result = num1 - num2
            elif self.operator == '*':
                result = num1 * num2
            elif self.operator == '/':
                if num2 == 0:
                    self.display_var.set("Infinity")
                    self.current_input = ""
                    self.result = ""
                    self.operator = ""
                    return
                result = num1 / num2
            
            # Set result
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10)).rstrip('0').rstrip('.')
            
            # Add to history
            self.add_to_history(expression, self.current_input)
            
            self.result = ""
            self.operator = ""
            self.waiting_for_operand = True
            self.update_display()
            
        except Exception as e:
            self.display_var.set("Error")
            self.current_input = ""
            self.result = ""
            self.operator = ""
    
    def clear_all(self):
        """Clear all data"""
        self.current_input = ""
        self.result = ""
        self.operator = ""
        self.waiting_for_operand = False
        self.display_var.set("0")
    
    def backspace(self):
        """Remove last digit"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
            self.update_display()
    
    def toggle_sign(self):
        """Toggle positive/negative sign"""
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def percentage(self):
        """Calculate percentage"""
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                if value.is_integer():
                    self.current_input = str(int(value))
                else:
                    self.current_input = str(value)
                self.update_display()
            except:
                self.display_var.set("Error")
                self.current_input = ""
    
    def reciprocal(self):
        """Reciprocal (1/x)"""
        if self.current_input and self.current_input != "0":
            try:
                value = 1 / float(self.current_input)
                if value.is_integer():
                    self.current_input = str(int(value))
                else:
                    self.current_input = str(round(value, 10))
                self.update_display()
            except:
                self.display_var.set("Error")
                self.current_input = ""
    
    def square_root(self):
        """Square root"""
        if self.current_input:
            try:
                value = float(self.current_input)
                if value >= 0:
                    result = math.sqrt(value)
                    self.current_input = str(round(result, 10))
                    self.update_display()
                else:
                    self.display_var.set("Imaginary Number")
            except:
                self.display_var.set("Error")
    
    def square(self):
        """Square (x²)"""
        if self.current_input:
            try:
                value = float(self.current_input)
                result = value ** 2
                self.current_input = str(round(result, 10))
                self.update_display()
            except:
                self.display_var.set("Error")
    
    def sine(self):
        """Sine function"""
        if self.current_input:
            try:
                value = float(self.current_input)
                result = math.sin(math.radians(value))  # Input in degrees
                self.current_input = str(round(result, 10))
                self.update_display()
            except:
                self.display_var.set("Error")
    
    def cosine(self):
        """Cosine function"""
        if self.current_input:
            try:
                value = float(self.current_input)
                result = math.cos(math.radians(value))  # Input in degrees
                self.current_input = str(round(result, 10))
                self.update_display()
            except:
                self.display_var.set("Error")
    
    def tangent(self):
        """Tangent function"""
        if self.current_input:
            try:
                value = float(self.current_input)
                result = math.tan(math.radians(value))  # Input in degrees
                self.current_input = str(round(result, 10))
                self.update_display()
            except:
                self.display_var.set("Error")
    
    def logarithm(self):
        """Logarithm (base 10)"""
        if self.current_input:
            try:
                value = float(self.current_input)
                if value > 0:
                    result = math.log10(value)
                    self.current_input = str(round(result, 10))
                    self.update_display()
                else:
                    self.display_var.set("Error: Number must be positive")
            except:
                self.display_var.set("Error")
    
    def pi(self):
        """Pi (π)"""
        self.current_input = str(math.pi)
        self.update_display()
    
    def euler(self):
        """Euler's number (e)"""
        self.current_input = str(math.e)
        self.update_display()
    
    def factorial(self):
        """Factorial"""
        if self.current_input:
            try:
                value = int(float(self.current_input))
                if value >= 0 and value <= 100:  # Limit for performance
                    result = math.factorial(value)
                    self.current_input = str(result)
                    self.update_display()
                elif value > 100:
                    self.display_var.set("Number too large")
                else:
                    self.display_var.set("Error: Negative number")
            except:
                self.display_var.set("Error")
    
    # Memory functions
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
        self.update_memory_display()
    
    def memory_recall(self):
        """Recall from memory"""
        self.current_input = str(self.memory)
        self.update_display()
    
    def memory_add(self):
        """Add to memory"""
        if self.current_input:
            try:
                self.memory += float(self.current_input)
                self.update_memory_display()
            except:
                pass
    
    def memory_subtract(self):
        """Subtract from memory"""
        if self.current_input:
            try:
                self.memory -= float(self.current_input)
                self.update_memory_display()
            except:
                pass
    
    def memory_store(self):
        """Store in memory"""
        if self.current_input:
            try:
                self.memory = float(self.current_input)
                self.update_memory_display()
            except:
                pass
    
    def update_memory_display(self):
        """Update memory display"""
        self.memory_label.config(text=f"Memory: {self.memory}")
    
    # History functions
    def add_to_history(self, expression, result):
        """Add to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            'time': timestamp,
            'expression': expression,
            'result': result
        }
        self.history.append(entry)
        
        # Keep only last 50 entries
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        # Save to file
        self.save_history()
    
    def show_history(self):
        """Show calculation history"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("400x500")
        history_window.configure(bg='#2e2e2e')
        
        # Title
        title_label = tk.Label(
            history_window,
            text="Calculation History",
            font=('Arial', 16, 'bold'),
            bg='#2e2e2e',
            fg='#ff9500'
        )
        title_label.pack(pady=10)
        
        # Text widget
        text_widget = tk.Text(
            history_window,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Arial', 10),
            wrap=tk.WORD,
            height=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Display history
        if not self.history:
            text_widget.insert(tk.END, "No history available\n")
        else:
            for entry in reversed(self.history):
                text = f"[{entry['time']}] {entry['expression']} = {entry['result']}\n"
                text_widget.insert(tk.END, text)
        
        text_widget.config(state=tk.DISABLED)
        
        # Clear button
        clear_btn = tk.Button(
            history_window,
            text="Clear History",
            font=('Arial', 12),
            bg='#ff9500',
            fg='#ffffff',
            command=lambda: self.clear_history(history_window)
        )
        clear_btn.pack(pady=10)
    
    def clear_history(self, window):
        """Clear history"""
        self.history = []
        self.save_history()
        window.destroy()
        messagebox.showinfo("Success", "History cleared")
    
    def save_history(self):
        """Save history to file"""
        try:
            with open('calculator_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_history(self):
        """Load history from file"""
        try:
            if os.path.exists('calculator_history.json'):
                with open('calculator_history.json', 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except:
            self.history = []
    
    # Theme functions
    def toggle_theme(self):
        """Toggle theme"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            # Dark theme
            self.current_theme = {
                'bg': '#2e2e2e',
                'fg': '#ffffff',
                'display_bg': '#1a1a1a',
                'button_bg': '#a5a5a5',
                'button_fg': '#000000',
                'operator_bg': '#ff9500',
                'special_bg': '#616161'
            }
        else:
            # Light theme
            self.current_theme = {
                'bg': '#f0f0f0',
                'fg': '#000000',
                'display_bg': '#ffffff',
                'button_bg': '#e0e0e0',
                'button_fg': '#000000',
                'operator_bg': '#ff9500',
                'special_bg': '#d0d0d0'
            }
        
        # Update all widgets
        self.update_theme()
    
    def update_theme(self):
        """Update theme"""
        # Main window
        self.root.configure(bg=self.current_theme['bg'])
        
        # Display
        self.display_frame.configure(bg=self.current_theme['bg'])
        self.display.configure(
            bg=self.current_theme['display_bg'],
            fg=self.current_theme['fg']
        )
        
        # Buttons frame
        self.buttons_frame.configure(bg=self.current_theme['bg'])
        
        # Memory label
        self.memory_label.configure(
            bg=self.current_theme['bg'],
            fg='#ff9500'  # Orange color won't change with theme
        )
    
    def update_display(self):
        """Update display"""
        if self.current_input:
            # Reduce font size for long numbers
            if len(self.current_input) > 15:
                self.display.config(font=('Arial', 18, 'bold'))
            else:
                self.display.config(font=self.display_font)
            
            self.display_var.set(self.current_input)
        else:
            self.display.config(font=self.display_font)
            if self.result and self.operator:
                # Operator mapping (for display)
                op_map = {'+': '+', '-': '-', '*': '×', '/': '÷'}
                display_op = op_map.get(self.operator, self.operator)
                self.display_var.set(f"{self.result} {display_op}")
            elif self.result:
                self.display_var.set(self.result)
            else:
                self.display_var.set("0")

def main():
    root = tk.Tk()
    app = AdvancedCalculator(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()