from utils import func

DATA_FILE = '../utils/operations.json'


def main():
    """
    Основной блок
    вывод на экран
    """
    for i in func.get_last_transaction(DATA_FILE):
        print(func.get_data_description(i))
        print(func.get_where_from(i))
        print(func.get_amount_currency(i))
        print()


if __name__ == '__main__':
    main()
