function deleteIncome(incomeId)
{
    fetch('/delete-income', {
        method: 'POST',
        body: JSON.stringify({ incomeId: incomeId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteExpense(expenseId)
{
    fetch('/delete-expense', {
        method: 'POST',
        body: JSON.stringify({ expenseId: expenseId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function updateExpense(expenseId) {
    const form = document.getElementById('form-' + expenseId);
    form.action = `/update_expense/${expenseId}`;
    form.submit();
}