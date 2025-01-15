from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_name = db.Column(db.String(150), nullable=False)
    expected_expense = db.Column(db.Float, nullable=False)
    actual_expense = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income_name = db.Column(db.String(150))
    expected_income = db.Column(db.Float)
    actual_income = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    expenses = db.relationship('Expense')
    incomes = db.relationship('Income')

    # Return the total budgetable income (sum of expected incomes).
    def get_total_income(self):
        return sum(income.expected_income for income in self.incomes)
    
    # Return the total earned income (sum of actual incomes)
    def get_total_actual_income(self):
        return sum(income.actual_income for income in self.incomes)
    
    # Return the total expenses.
    def get_total_expenses(self):
        return sum(expense.expected_expense for expense in self.expenses)
    
    # Return the remaining to budget.
    def get_remaining_to_budget(self):
        return self.get_total_income() - self.get_total_expenses()
    
    # Return the total actual spent.
    def get_actual_spent(self):
        return sum(expense.actual_expense for expense in self.expenses)
    
    # Return the difference in actual income and actual spent.
    def get_difference(self):
        return (self.get_total_actual_income() - self.get_actual_spent())
