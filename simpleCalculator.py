from __future__ import annotations
from typing import Callable, Iterable, List, Tuple
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

Number = float

def parse_number_list(raw: str) -> List[Number]:
    raw = raw.strip()
    if not raw:
        return []
    tokens = []
    for part in raw.replace(",", " ").split():
        tokens.append(part)
    numbers: List[Number] = []
    for t in tokens:
        try:
            numbers.append(float(t))
        except ValueError as e:
            raise ValueError(f"Invalid number: '{t}'") from e
    return numbers

def require_min_numbers(nums: List[Number], min_count: int = 2) -> None:
    if len(nums) < min_count:
        raise ValueError(f"Please enter at least {min_count} number(s).")

def safe_div(a: Number, b: Number) -> Number:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by 0")
    return a / b

def safe_mod(a: Number, b: Number) -> Number:
    if b == 0:
        raise ZeroDivisionError("Cannot mod by 0")
    return a % b

def reduce_left(nums: Iterable[Number], op: Callable[[Number, Number], Number]) -> Number:
    it = iter(nums)
    try:
        acc = next(it)
    except StopIteration:
        raise ValueError("No numbers provided")
    for x in it:
        acc = op(acc, x)
    return acc

def apply_operation(nums: List[Number], operation_key: str) -> Number:
    if operation_key == "+":
        return reduce_left(nums, lambda a, b: a + b)
    if operation_key == "-":
        return reduce_left(nums, lambda a, b: a - b)
    if operation_key == "*":
        return reduce_left(nums, lambda a, b: a * b)
    if operation_key == "/":
        return reduce_left(nums, safe_div)
    if operation_key == "**":
        return reduce_left(nums, lambda a, b: a**b)
    if operation_key == "%":
        return reduce_left(nums, safe_mod)
    raise ValueError("Unknown operation")

def format_number(n: Number) -> str:
    if abs(n - round(n)) < 1e-12:
        return str(int(round(n)))
    return str(n)

# GUI
class CalculatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        self.history: List[Tuple[str, str, str, str]] = []  # (timestamp, expression, result, operation)
        
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.button_bg = "#4a4a4a"
        self.button_fg = "#ffffff"
        self.history_bg = "#1e1e1e"
        self.history_fg = "#00ff00"
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        
    def setup_ui(self):
        title_label = tk.Label(
            self.root,
            text="BaseCalc Calculator",
            font=("Verdana", 20, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(pady=10, padx=20, fill="both")
        op_frame = tk.LabelFrame(main_frame, text="Select Operation", bg=self.bg_color, fg=self.fg_color, font=("Verdana", 12, "bold"))
        op_frame.pack(fill="x", pady=5)
        
        self.operation_var = tk.StringVar(value="+")
        
        operations = [
            ("Addition (+)", "+"),
            ("Subtraction (-)", "-"),
            ("Multiplication (*)", "*"),
            ("Division (/)", "/"),
            ("Exponentiation (**)", "**"),
            ("Modulus (%)", "%")
        ]
        
        for i, (text, op) in enumerate(operations):
            rb = tk.Radiobutton(
                op_frame,
                text=text,
                variable=self.operation_var,
                value=op,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor=self.bg_color,
                font=("Inter", 10)
            )
            rb.grid(row=i//3, column=i%3, sticky="w", padx=10, pady=5)
        
        input_frame = tk.LabelFrame(main_frame, text="Enter Numbers", bg=self.bg_color, fg=self.fg_color, font=("Verdana", 12, "bold"))
        input_frame.pack(fill="x", pady=10)
        
        tk.Label(
            input_frame,
            text="Enter numbers separated by commas or spaces:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Inter", 10)
        ).pack(anchor="w", padx=10, pady=5)
        
        self.numbers_entry = tk.Text(input_frame, height=3, width=50, font=("Arial", 10))
        self.numbers_entry.pack(padx=10, pady=5, fill="x")
        
        example_frame = tk.Frame(input_frame, bg=self.bg_color)
        example_frame.pack(pady=5)
        
        tk.Button(
            example_frame,
            text="Example: 2, 3, 4",
            command=self.insert_example,
            bg="#5a5a5a",
            fg=self.fg_color,
            font=("Poppins", 9)
        ).pack(side="left", padx=5)
        
        tk.Button(
            example_frame,
            text="Clear",
            command=self.clear_numbers,
            bg="#5a5a5a",
            fg=self.fg_color,
            font=("Arial", 9)
        ).pack(side="left", padx=5)
        
        # Calculate button
        self.calc_button = tk.Button(
            main_frame,
            text="CALCULATE",
            command=self.calculate,
            bg="#42A036",
            fg="white",
            font=("Poppins", 14, "bold"),
            height=2,
            cursor="hand2"
        )
        self.calc_button.pack(pady=10, fill="x")
        
        result_frame = tk.LabelFrame(main_frame, text="Result", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12, "bold"))
        result_frame.pack(fill="x", pady=10)
        
        self.result_label = tk.Label(
            result_frame,
            text="Ready",
            bg=self.bg_color,
            fg="#4CAF50",
            font=("Verdana", 16, "bold"),
            height=2
        )
        self.result_label.pack(pady=10)
        
        history_frame = tk.LabelFrame(self.root, text="Calculation History", bg=self.bg_color, fg=self.fg_color, font=("Arial", 12, "bold"))
        history_frame.pack(fill="both", expand=True, pady=10, padx=20)
        
        history_buttons_frame = tk.Frame(history_frame, bg=self.bg_color)
        history_buttons_frame.pack(pady=5)
        
        tk.Button(
            history_buttons_frame,
            text="Clear History",
            command=self.clear_history,
            bg="#ff4444",
            fg="white",
            font=("Inter", 10),
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            history_buttons_frame,
            text="Export History",
            command=self.export_history,
            bg="#2196F3",
            fg="white",
            font=("Inter", 10),
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        history_list_frame = tk.Frame(history_frame, bg=self.bg_color)
        history_list_frame.pack(fill="both", expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(history_list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(
            history_list_frame,
            bg=self.history_bg,
            fg=self.history_fg,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        self.history_listbox.bind("<Double-Button-1>", self.reuse_calculation)
        
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def insert_example(self):
        self.numbers_entry.delete("1.0", tk.END)
        self.numbers_entry.insert("1.0", "2, 3, 4")
        self.update_status("Example numbers inserted")
    
    def clear_numbers(self):
        self.numbers_entry.delete("1.0", tk.END)
        self.update_status("Numbers cleared")
    
    def calculate(self):
        raw_nums = self.numbers_entry.get("1.0", tk.END).strip()
        operation_key = self.operation_var.get()
        
        try:
            nums = parse_number_list(raw_nums)
            require_min_numbers(nums, 2)
            result = apply_operation(nums, operation_key)
            
            formatted_result = format_number(result)
            self.result_label.config(text=formatted_result, fg="#4CAF50")
            
            op_symbols = {"+": " + ", "-": " - ", "*": " × ", "/": " ÷ ", "**": "^", "%": " % "}
            op_display = op_symbols.get(operation_key, f" {operation_key} ")
            
            expr = op_display.join([format_number(n) for n in nums])
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            self.add_to_history(timestamp, expr, formatted_result, operation_key)
            
            self.update_status(f"Calculation successful: {expr} = {formatted_result}")
            
        except ValueError as e:
            self.result_label.config(text="Error", fg="#ff4444")
            messagebox.showerror("Input Error", str(e))
            self.update_status(f"Error: {e}")
        except ZeroDivisionError as e:
            self.result_label.config(text="Error", fg="#ff4444")
            messagebox.showerror("Math Error", str(e))
            self.update_status(f"Error: {e}")
    
    def add_to_history(self, timestamp: str, expression: str, result: str, operation: str):
        history_entry = f"[{timestamp}] {expression} = {result}"
        self.history_listbox.insert(0, history_entry)
        self.history.insert(0, (timestamp, expression, result, operation))
        
        if len(self.history) > 50: #history limit
            self.history.pop()
            self.history_listbox.delete(50)
    
    def clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.history.clear()
            self.history_listbox.delete(0, tk.END)
            self.update_status("History cleared")
    
    def export_history(self):
        if not self.history:
            messagebox.showwarning("No History", "No calculations to export.")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"calculator_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("BaseCalc Calculator History\n")
                    f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*50 + "\n\n")
                    
                    for i, (timestamp, expression, result, operation) in enumerate(self.history, 1):
                        f.write(f"{i}. [{timestamp}] {expression} = {result}\n")
                
                self.update_status(f"History exported to {filename}")
                messagebox.showinfo("Export Successful", f"History saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export history:\n{e}")
    
    def reuse_calculation(self, event):
        """Double-click on a history item to reuse that calculation"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.history):
                timestamp, expression, result, operation = self.history[index]
                
                numbers_str = expression.replace(" + ", ",").replace(" - ", ",").replace(" × ", ",")
                numbers_str = numbers_str.replace(" ÷ ", ",").replace("^", ",").replace(" % ", ",")
                
                self.numbers_entry.delete("1.0", tk.END)
                self.numbers_entry.insert("1.0", numbers_str)
                self.operation_var.set(operation)
                self.update_status(f"Loaded calculation from history: {expression}")
                
                if messagebox.askyesno("Auto-calculate", "Would you like to calculate this now?"):
                    self.calculate()
    
    def update_status(self, message: str):
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready")) 


def main():
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
