import tkinter as tk
from tkinter import ttk, messagebox
from finance_manager import FinanceManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.fm = FinanceManager()

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')

        # Add tabs
        self.create_add_transaction_tab()
        self.create_summary_tab()
        self.create_report_tab()

    def create_add_transaction_tab(self):
        self.add_transaction_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_transaction_frame, text='Add Transaction')

        # Transaction Type
        ttk.Label(self.add_transaction_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.transaction_type = ttk.Combobox(self.add_transaction_frame, values=['Income', 'Expense', 'Saving'])
        self.transaction_type.grid(row=0, column=1, padx=5, pady=5)
        self.transaction_type.set('Expense')

        # Amount
        ttk.Label(self.add_transaction_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.add_transaction_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Category (for expenses)
        ttk.Label(self.add_transaction_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.add_transaction_frame)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        # Description
        ttk.Label(self.add_transaction_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.add_transaction_frame)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5)

        # Date
        ttk.Label(self.add_transaction_frame, text="Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.add_transaction_frame)
        self.date_entry.grid(row=4, column=1, padx=5, pady=5)

        # Add Button
        ttk.Button(self.add_transaction_frame, text="Add Transaction", command=self.add_transaction).grid(row=5, columnspan=2, pady=10)

    def create_summary_tab(self):
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text='Summary')

        self.summary_text = tk.Text(self.summary_frame, height=10, width=50)
        self.summary_text.pack(pady=10, padx=10)
        self.update_summary()

    def create_report_tab(self):
        self.report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.report_frame, text='Expense Report')

        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.report_frame)
        self.canvas.get_tk_widget().pack()
        self.update_report()

    def add_transaction(self):
        ttype = self.transaction_type.get()
        amount = float(self.amount_entry.get())
        description = self.description_entry.get()
        date = self.date_entry.get()

        if ttype == 'Income':
            self.fm.add_income(amount, description, date)
        elif ttype == 'Expense':
            category = self.category_entry.get()
            self.fm.add_expense(amount, category, description, date)
        elif ttype == 'Saving':
            self.fm.add_saving(amount, description, date)

        messagebox.showinfo("Success", "Transaction added successfully.")
        self.update_summary()
        self.update_report()

    def update_summary(self):
        summary = self.fm.get_financial_summary()
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert(tk.END, f"Total Income: {summary['total_income']}\n")
        self.summary_text.insert(tk.END, f"Total Expense: {summary['total_expense']}\n")
        self.summary_text.insert(tk.END, f"Total Savings: {summary['total_savings']}\n")
        self.summary_text.insert(tk.END, f"Balance: {summary['balance']}\n")

    def update_report(self):
        self.ax.clear()
        expenses = self.fm.get_expenses()
        if not expenses:
            self.ax.text(0.5, 0.5, "No expenses to report.", ha='center', va='center')
            self.canvas.draw()
            return

        categories = {}
        for expense in expenses:
            category = expense[2]
            amount = expense[1]
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        self.ax.bar(categories.keys(), categories.values())
        self.ax.set_xlabel("Category")
        self.ax.set_ylabel("Amount")
        self.ax.set_title("Expense Report by Category")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
