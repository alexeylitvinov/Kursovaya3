import json
import os.path
from datetime import datetime


def get_last_transaction(file_name) -> list:
    data_base = []
    last_transaction = []
    with open(os.path.abspath(file_name), 'r', encoding='utf-8') as file:
        for i in json.load(file):
            if i.get('state') == 'EXECUTED':
                data_base.append(i)
    for i in sorted(data_base, key=lambda x: x['date'], reverse=True):
        last_transaction.append(i)
        if len(last_transaction) == 5:
            break
    return last_transaction


def get_data_description(transaction: dict) -> str:
    user_data = datetime.fromisoformat(transaction['date'])
    return f'{user_data.strftime('%d.%m.%Y')} {transaction['description']}'


def get_where_from(transaction: dict) -> str:
    if transaction.get('from') is None:
        transaction['from'] = 'Внесение наличности на счет'
    ls1 = transaction['from'].split(' ')
    ls2 = transaction['to'].split(' ')
    if len(ls1[-1]) == 16 and ls1[-1].isdigit:
        ls1[-1] = ls1[-1][:4] + ' ' + ls1[-1][4:6] + '** **** ' + ls1[-1][-4:]
    elif len(ls1[-1]) > 16 and ls1[-1].isdigit:
        ls1[-1] = '**' + ls1[-1][-4:]
    if len(ls2[-1]) == 16 and ls2[-1].isdigit:
        ls2[-1] = ls2[-1][:4] + ' ' + ls2[-1][4:6] + '** **** ' + ls2[-1][-4:]
    elif len(ls2[-1]) > 16 and ls2[-1].isdigit:
        ls2[-1] = '**' + ls2[-1][-4:]
    return f'{' '.join(ls1)} -> {' '.join(ls2)}'


def get_amount_currency(transaction: dict) -> str:
    return f'{transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['name']}'
