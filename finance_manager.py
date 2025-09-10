from database import Database

class FinanceManager:
    def __init__(self, db_path='personal_finance.db'):
        self.db = Database(db_path)

    def add_income(self, amount, description, date):
        self.db.add_income(amount, description, date)

    def add_expense(self, amount, category, description, date):
        self.db.add_expense(amount, category, description, date)

    def add_saving(self, amount, description, date):
        self.db.add_saving(amount, description, date)

    def get_incomes(self):
        return self.db.get_incomes()

    def get_expenses(self):
        return self.db.get_expenses()

    def get_savings(self):
        return self.db.get_savings()

    def get_financial_summary(self):
        incomes = self.get_incomes()
        expenses = self.get_expenses()
        savings = self.get_savings()

        total_income = sum(income[1] for income in incomes)
        total_expense = sum(expense[1] for expense in expenses)
        total_savings = sum(saving[1] for saving in savings)

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'total_savings': total_savings,
            'balance': total_income - total_expense - total_savings
        }
