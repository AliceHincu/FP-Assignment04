"""
Domain file includes code for entity management
entity = number, transaction, expense etc.
"""


# ---- getters / setters ----


def get_day(expense):
    '''
    Gets the day
    :param expense: the expense (type: dictionary)
    :return: the day (type: int)
    '''
    return expense.get("day")


def get_money(expense):
    '''
    Gets the money value
    :param expense: the expense (type: dictionary)
    :return: the amount of money (type: int)
    '''
    return expense.get("amount_of_money")


def get_type(expense):
    '''
    Gets the type of expense
    :param expense: the expense (type: dictionary)
    :return: the expense type (type: string)
    '''
    return expense.get("expense_type")


def set_money(expense, value):
    '''
    Gets the money value
    :param expense: the expense (type: dictionary)
    :param value: the value that needs to be added
    :return: Nothing
    '''
    expense["amount_of_money"] += value


def check_type(nr):
    '''
    -We check what type the variable is
    -To be correct, it need to be either a natural number or a string of the expense type
    -If not, it raises an error
    :param nr: the parameter that we want to check (type: string)
    :return: the type (type: string)
    '''
    try:  # if it is a number or not
        nr = float(nr)
    except ValueError:
        expense_dict = ['housekeeping', 'food', 'transport', 'clothing', 'internet', 'others']
        if nr not in expense_dict:
            raise ValueError("This is not an available type of expense or a number!\n\tAvailable types:"
                             "housekeeping, food, transport, clothing, internet, others\n"
                             "Please try again!")
        return 'string'

    if nr.is_integer():  # if it is int or float
        nr = int(nr)
        if nr >= 0:  # if it is positive or not
            return 'natural'
        else:
            raise ValueError("This is a negative number! Try again...")
    else:
        raise ValueError("This is a float number! Try again...")


def create_expense(day, money, type):
    '''
    -We check if the inserted expense is good
    -If it is good, we create the expense and return it. If not, errors will appear
    :param day: the day (type: int(positive))
    :param money: the amount of money (type: int(positive))
    :param type: the type of expense (type: string)
    :return: the expense (type: dictionary)
    '''

    # day: between 1 and 30, for simplicity
    if check_type(day) == 'natural':
        day = int(day)
    if day < 1 or day > 30:
        raise ValueError('The day is not in the interval [1,30]! Try again...')

    # amount of money :positive integer
    if check_type(money) == 'natural':
        money = int(money)

    # expense type: housekeeping, food, transport, clothing, internet, others)
    if check_type(type) == 'string':
        type = str(type)

    return {'day': int(day), 'amount_of_money': int(money), 'expense_type': str(type)}
