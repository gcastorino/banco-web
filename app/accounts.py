from flask import Blueprint, render_template, request, redirect, url_for
from Models.accounts import Account
from db import Database

account_app = Blueprint('accounts_app',__name__,url_prefix='/accounts')

@account_app.route('/form')
def form():
    return render_template('form.html')

@account_app.route('/list', methods=['GET'])
def get_account():
    sql = "select * from contas"
    accounts = []
    for registro in Database().getall(sql):
        account = Account(registro[1], registro[2], registro[3], registro[4], registro[0])
        accounts.append(account)
    return render_template('lista.html', contas = accounts)

@account_app.route('/account', methods=['POST'])
def post_account():
    new_account = request.form
    account = Account(new_account.get('numero'),new_account.get('titular'), float(new_account.get('saldo')),
                      float(new_account.get('limite')))
    sql = "insert into contas (id, numero, titular, saldo, limite) values (%s, %s, %s, %s, %s)"
    valores = (str(account.id), account.numero, account.titular, account.saldo, account.limite)
    operation = Database().insert(sql,valores)
    print(operation)
    return redirect(url_for('accounts_app.get_account'))
