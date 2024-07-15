from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Income
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        income_name = request.form.get('incomeName')
        expected_income = float(request.form.get('expectedIncome'))
        actual_income = float(request.form.get('actualIncome'))
        
        if len(income_name) < 1:
            flash('Must give income a name. Try again.', category='error')
        elif expected_income < 0:
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

    return render_template("home.html", user=current_user)

