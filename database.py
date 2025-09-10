import sqlite3

class Database:
    def __init__(self, db_path='personal_finance.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS incomes (
                    id INTEGER PRIMARY KEY,
                    amount REAL NOT NULL,
                    description TEXT,
                    date TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    amount REAL NOT NULL,
                    category TEXT,
                    description TEXT,
                    date TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS savings (
                    id INTEGER PRIMARY KEY,
                    amount REAL NOT NULL,
                    description TEXT,
                    date TEXT
                )
            """)

    def add_income(self, amount, description, date):
        with self.conn:
            self.conn.execute("INSERT INTO incomes (amount, description, date) VALUES (?, ?, ?)", (amount, description, date))

    def add_expense(self, amount, category, description, date):
        with self.conn:
            self.conn.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)", (amount, category, description, date))

    def add_saving(self, amount, description, date):
        with self.conn:
            self.conn.execute("INSERT INTO savings (amount, description, date) VALUES (?, ?, ?)", (amount, description, date))

    def get_incomes(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM incomes").fetchall()

    def get_expenses(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM expenses").fetchall()

    def get_savings(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM savings").fetchall()
