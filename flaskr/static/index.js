function deleteIncome(incomeId)
{
    fetch('/delete-income', {
        method: 'POST',
        body: JSON.stringify({ incomeId: incomeId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function updateIncome(incomeId) {
	const form = document.getElementById('form-' +incomeId);
	form.action = `/update_income/${incomeId}`;
	form.submit();
}

function updateExpense(expenseId) {
    const form = document.getElementById('form-' +expenseId);
    form.action = `/update_expense/${expenseId}`;
    form.submit();
}

function deleteExpense(expenseId) {
    fetch('/delete-expense', {
        method: 'POST',
        body: JSON.stringify({ expenseId: expenseId }),
    }).then((_res) => {
        window.location.href = "/expenses";
    });
}

