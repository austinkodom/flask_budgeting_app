from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Income
from .models import Expense
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'expenseName' in request.form:
            addExpense()
        if 'incomeName' in request.form:
            addIncome()
        
    return render_template(
        "home.html", 
        user=current_user, 
        total_income=get_total_income(),
        remaining_to_budget=get_remaining_to_budget())

@views.route('/delete-income', methods=['POST'])
def delete_income():
    income = json.loads(request.data)
    income_id = income['incomeId']
    income = Income.query.get(income_id)

    if income:
        if income.user_id == current_user.id:
            db.session.delete(income)
            db.session.commit()

    return jsonify({})

@views.route('delete-expense', methods=['POST'])
def delete_expense():
    expense = json.loads(request.data)
    expense_id = expense['expenseId']
    expense = Expense.query.get(expense_id)

    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()

    return jsonify({})

def addIncome():
    income_name = request.form.get('incomeName')
    expected_income = float(request.form.get('expectedIncome'))
    actual_income = float(request.form.get('actualIncome'))
        
    if len(income_name) < 1:
        flash('Must give income a name. Try again.', category='error')
    elif expected_income < 0 or expected_income == 0:
        flash('Income must be greater than 0', category='error')
    else:
        new_income = Income(
            income_name = income_name,
            expected_income = expected_income,
            actual_income = actual_income,
            user_id = current_user.id
        )

        db.session.add(new_income)
        db.session.commit()

        flash('Income successfully added.', category='success')

def addExpense():
    expense_name = request.form.get('expenseName')
    expected_expense = float(request.form.get('expectedExpense'))
    actual_expense = float(request.form.get('actualExpense'))
        
    if len(expense_name) < 1:
        flash('Must give expense a name. Try again.', category='error')
    elif expected_expense < 0 or expected_expense == 0:
        flash('Expense must be greater than 0. Try again', category='error')
    else:
        new_expense = Expense(                
            expense_name = expense_name,
            expected_expense = expected_expense,
            actual_expense = actual_expense,
            user_id = current_user.id
        )

        db.session.add(new_expense)
        db.session.commit()

        flash('Expense successfully added.', category='success')

def get_total_income():
    incomes = Income.query.with_entities(Income.expected_income).all()
    total_income = sum(income.expected_income for income in incomes)
    return total_income

def get_total_expenses():
    expenses = Expense.query.with_entities(Expense.expected_expense).all()
    total_expenses = sum(expense.expected_expense for expense in expenses)
    return total_expenses

def get_remaining_to_budget():
    total_income = get_total_income()
    total_expenses = get_total_expenses()
    remaining_to_budget = total_income - total_expenses
    return remaining_to_budget