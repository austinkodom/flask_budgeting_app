from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Income
from .models import Expense
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/update_expense/<int:expense_id>', methods=['POST'])
def update_expense(expense_id):
    actual_expense = float(request.form.get('actualExpense'))
    expense = Expense.query.get(expense_id)
    if expense:
        expense.actual_expense = actual_expense
        db.session.commit()
    return redirect(url_for('views.expenses'))

# Method to update expenses as they may change, or
# the amount may differ from what was expected.
@views.route('/update_income/<int:income_id>', methods=['POST'])
def update_income(income_id):
    actual_income = request.form.get('actualIncome')
    income = Income.query.get(income_id)
    if income:
        income.actual_income = actual_income
        db.session.commit()
    else:
        flash('An error has occurred.', category='error')
    return redirect(url_for('views.home'))

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
        total_income=current_user.get_total_income(),
        remaining_to_budget=current_user.get_remaining_to_budget(),
        actual_spent=current_user.get_actual_spent(),
        difference=current_user.get_difference()
    )

@views.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    if request.method == 'POST':
        addExpense()  

    return render_template(
        "expenses.html",
        user=current_user, 
        total_income=current_user.get_total_income(),
        remaining_to_budget=current_user.get_remaining_to_budget(),
        actual_spent=current_user.get_actual_spent(),
        difference=current_user.get_difference()
    )

@views.route('/how-to')
def how_to_use():
    return render_template("how_to_use.html", user=current_user)


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

@views.route('/delete-expense', methods=['POST'])
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
    elif actual_expense < 0:
        flash('Actual expense must be not be negative.', category='error')
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
