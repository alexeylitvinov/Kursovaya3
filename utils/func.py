import json
from datetime import datetime


def get_last_transaction(file_name) -> list:
    """
    Возвращает из .json файла последние 5 транзакций, отбрасывает отмененные операции и
    сортирует по дате
    :param file_name: file name
    :return: list
    """
    data_base = []
    last_transaction = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for i in json.load(file):
            if i.get('state') == 'EXECUTED':
                data_base.append(i)
    for i in sorted(data_base, key=lambda x: x['date'], reverse=True):
        last_transaction.append(i)
        if len(last_transaction) == 5:
            break
    return last_transaction


def get_data_description(transaction: dict) -> str:
    """
    Переводит дату из словаря в формат ДД.ММ.ГГГГ и возвращает в строке дату и операцию
    :param transaction: dict
    :return: str
    """
    user_data = datetime.fromisoformat(transaction['date'])
    return f'{user_data.strftime('%d.%m.%Y')} {transaction['description']}'


def get_where_from(transaction: dict) -> str:
    """
    Берет из словаря операции "откуда и куда", прячет номера счетов и карточек c помощью функции
    get_hide_number и возвращает это в строке
    :param transaction: dict
    :return: str
    """
    if transaction.get('from') is None:
        transaction['from'] = 'Внесение наличности на счет'
    ls1 = transaction['from'].split(' ')
    ls2 = transaction['to'].split(' ')

    def get_hide_number(lst: list) -> str:
        """
        Получает список транзакции из функции get_where_from и прячет номера счетов и карточек
        возвращает строку
        :param lst: list
        :return: str
        """
        if len(lst[-1]) == 16 and lst[-1].isdigit():
            lst[-1] = lst[-1][:4] + ' ' + lst[-1][4:6] + '** **** ' + lst[-1][-4:]
        elif len(lst[-1]) > 16 and lst[-1].isdigit():
            lst[-1] = '**' + lst[-1][-4:]
        return ' '.join(lst)

    return f'{get_hide_number(ls1)} -> {get_hide_number(ls2)}'


def get_amount_currency(transaction: dict) -> str:
    """
    Возвращает из словаря транзакций строку с суммой и валютой операции
    :param transaction: dict
    :return: str
    """
    return f'{transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['name']}'
