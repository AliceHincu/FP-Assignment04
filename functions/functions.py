from datetime import date
from domain.entity import get_type, get_day, get_money, set_money, check_type, create_expense
from ui.console import display_by_category2, display_by_days2, display_none, display_none2, \
    display_by_category_compare2, print_sum, print_max_day, display_list

from copy import deepcopy

# ----- Functions that implement program features. They should call each other, or other functions from the domain -----


# ---- add functions ----
def is_in_list(day, type, expenses):
    """
    Checks if there are 2 expenses in the same day for the same type
    :param day: the day (type: int)
    :param type: the category (type: string)
    :param expenses: the list of expenses (type: list)
    :return: Nothing
    """
    for i in range(len(expenses)):
        if get_day(expenses[i]) == int(day):
            if get_type(expenses[i]) == type:
                return i
    return -1


def add_new_expense(expenses, command_param, history_list):
    '''
    We add a new expense to the list in the current day
    :param expenses: the list of expenses (type: list)
    :param command_param: the parameters of the command (type: list)
    :param history_list: the history list (type: list)
    :return: Nothing
    '''

    if len(command_param) == 2:
        day = str(date.today())
        tokens = day.split("-")
        day = int(tokens[2])  # current day
        result = int(is_in_list(day, command_param[1], expenses))
        if result == -1:
            expenses.append(create_expense(day, command_param[0], command_param[1]))
        else:
            set_money(expenses[result], int(command_param[0]))
        ex_copy = deepcopy(expenses)
        history_list.append(ex_copy)
    else:
        raise ValueError("Wrong input! See the available options:\n"
                         "\tadd <sum> <category>\n")


def insert_new_expense(expenses, command_param, history_list):
    '''
    Insert to day x an expense of certain money
    :param expenses: the list of expenses (type: list)
    :param command_param: the parameters (type: list)
    :param history_list: the history list (type: list)
    :return: Nothing
    '''
    if len(command_param) == 3:
        if not is_in_list(command_param[0], command_param[2], expenses):
            expenses.append(create_expense(command_param[0], command_param[1], command_param[2]))
            ex_copy = expenses[:]
            history_list.append(ex_copy)
    else:
        raise ValueError("Wrong input! See the available options:"
                         "\n\tinsert <day> <sum> <category>\n")


# ---- modify functions ----
def m_what_command(command_param):
    '''
    -We check if the parameters for the modify functions are correct.
    -If they are, we find out what command the user wants (from the 3 available commands)
    :param command_param: list of parameters (type: list)
    :return: the number of the command (type: int)
    '''

    if len(command_param) == 1:
        type = check_type(command_param[0])
        if type == 'natural':
            return 1
        elif type == 'string':
            return 3
    elif len(command_param) == 3:
        type1 = check_type(command_param[0])
        type2 = check_type(command_param[2])
        if command_param[1] == 'to' and type1 == type2 == 'natural':
            if 0 < int(command_param[0]) < 31 and 0 < int(command_param[2]) < 31:
                return 2
            else:
                raise ValueError("The days are in the interval [1, 30]! Try again...")
        else:
            raise ValueError("Wrong parameters!")
    else:
        raise ValueError("Wrong input! See the available options:"
                         "\n\tremove <day>\n\tremove <start day> to <end day>"
                         "\n\tremove <category>")


def remove(begin, end, step, expenses, x_to_delete, x):
    '''
    Does the deleting from the list
    :param begin: the beginning of the "for" index (type:int)
    :param end: the end of the "for" index (type:int)
    :param step: the step of the "for" index (type:int)
    :param expenses: the list of the expenses
    :param x_to_delete: the value we looking for to delete
    :param x: the element(day,money,category) that we are looking for so we can delete
    :return: Nothing
    '''
    if x == 'day':
        for i in range(begin, end, step):  # remove from list the dict
            if get_day(expenses[i]) == x_to_delete:
                expenses.pop(i)
    else:
        for i in range(begin, end, step):  # remove from list the dict
            if get_type(expenses[i]) == x_to_delete:
                expenses.pop(i)


def modify_expenses(expenses, command_param, history_list):
    '''
    It modifies the expenses. For:
    - p=1 : remove <day>
    - p=2 : remove <start day> to <end day>
    - p=3 : remove <category>
    :param expenses: list of expenses (type: list)
    :param command_param: parameters (type: list)
    :param history_list: the history list (type: list)
    :return: Nothing
    '''
    p = m_what_command(command_param)
    if p == 1:
        # remove < day >
        day_to_delete = int(command_param[0])  # what day to remove
        remove(len(expenses)-1, -1, -1, expenses, day_to_delete, 'day')  # do the removing

    elif p == 2:
        # remove <start day> to <end day>
        from_day = int(command_param[0])  # from what day
        to_day = int(command_param[2])  # until that day
        for day_to_delete in range(from_day, to_day+1):
            remove(len(expenses)-1, -1, -1, expenses, day_to_delete, 'day')  # do the removing

    elif p == 3:
        # remove <category>
        category_to_delete = command_param[0]
        remove(len(expenses)-1, -1, -1, expenses, category_to_delete, 'category')  # do the removing

    ex_copy = expenses[:]
    history_list.append(ex_copy)


# ---- display functions ----


def d_what_command(command_param):
    '''
    -We check if the parameters for the display functions are correct.
    -If they are, we find out what command the user wants (from the 5 available commands)
    :param command_param: list of parameters (type: list)
    :return: the number of the command (type: int)
    '''
    if len(command_param) == 0:
        return 1
    if len(command_param) == 1 and check_type(command_param[0]) == 'string':
        return 2
    if len(command_param) == 3 and check_type(command_param[0]) == 'string' and\
            check_type(command_param[2]) == 'natural':
        if command_param[1] == '<':
            return 3
        elif command_param[1] == '=':
            return 4
        elif command_param[1] == '>':
            return 5
        else:
            raise ValueError("Choose from <,=,>")
    else:
        raise ValueError("Wrong input! See the available options:"
                         "\n\tlist\n\tlist <category>"
                         "\n\tlist <category> [ < | = | > ] <value>")


def display_by_days(expenses):
    '''
    We display the expenses ordered by the day
    :param expenses: list of expenses (type: list)
    :return: Nothing
    '''
    expenses2 = []
    for i in range(1, 31):
        day_print = False  # if the day was not printed
        for j in range(len(expenses)):
            if get_day(expenses[j]) == i:
                if not day_print:
                    expenses2.append(expenses[j])
    display_by_days2(expenses2)


def display_by_category(category, expenses):
    '''
    We display the expenses ordered by the category
    :param expenses: list of expenses (type: list)
    :param category: the category we are looking for (type: string)
    :return: Nothing
    '''
    expenses2 = []
    exists = False
    for i in range(1, 31):
        for j in range(len(expenses)):
            if get_day(expenses[j]) == i and get_type(expenses[j]) == category:
                expenses2.append(expenses[j])
                exists = True

    if not exists:
        display_none(category)
    else:
        display_by_category2(expenses2)


def display_by_category_compare(category, value, expenses, p):
    '''
    We display the expenses ordered by the category
    :param expenses: list of expenses (type: list)
    :param value: the value we use to compare
    :param category: the category we are looking for (type: string)
    :param p: - for p=3 -> we use '<'
              - for p=4 -> we use '='
              - for p=5 -> we use '>'
    :return: Nothing
    '''
    expenses2 = []
    exists = False

    for i in range(1, 31):
        for j in range(len(expenses)):
            if get_day(expenses[j]) == i and get_type(expenses[j]) == category:
                if p == 3 and get_money(expenses[j]) < int(value):
                    expenses2.append(expenses[j])
                    exists = True
                elif p == 4 and get_money(expenses[j]) == int(value):
                    expenses2.append(expenses[j])
                    exists = True
                elif p == 5 and get_money(expenses[j]) > int(value):
                    expenses2.append(expenses[j])
                    exists = True

    if not exists:
        display_none2(p, category, value)
    else:
        display_by_category_compare2(expenses2)


def display_expenses(_expenses, command_param, history_list):
    '''
    Displays what you asked based on the input
    p1: list
    p2: list <category>
    [ p3 | p4 | p5 ]: list <category> [ < | = | > ] <value>
    :param _expenses: list of expenses (type: list)
    :param command_param: list of parameters (type: list)
    :param history_list: the history list (type: list)
    :return: Nothing
    '''
    p = d_what_command(command_param)
    expenses2 = list(history_list[len(history_list)-1])
    if p == 1:
        display_by_days(expenses2)
    elif p == 2:
        display_by_category(command_param[0], expenses2)
    else:
        display_by_category_compare(command_param[0], command_param[2], expenses2, p)


# ---- different characteristics ----


def summ(expenses, category):
    '''
    Calculates the total expense for a category
    :param expenses: list of expenses (type: list)
    :param category: the category (type: string)
    :return: the sum (type: int)
    '''
    sum = 0
    for i in range(len(expenses)):
        if str(get_type(expenses[i])) == str(category):
            sum += int(get_money(expenses[i]))
    return sum


def sum_expenses(expenses, command_param, _history_list):
    '''
    Displays the total expense for a category
    :param expenses: list of expenses (type: list)
    :param command_param: the category (type: list)
    :param _history_list: the history list (type: list)
    :return: Nothing
    '''
    if not check_type(command_param[0]) == 'string' or not len(command_param) == 1:
        raise ValueError('Wrong input!')
    sum = summ(expenses, command_param[0])
    print_sum(sum, command_param[0])


def maxx(expenses):
    '''
    Calculates the max day
    :param expenses: list of expenses (type: list)
    :return: the max day (type: int)
    '''
    max_day = 0
    max_sum = 0
    for day in range(1, 31):
        sum = 0
        for i in range(len(expenses)):
            if get_day(expenses[i]) == day:
                sum += get_money(expenses[i])
        if max_sum < sum:
            max_sum = sum
            max_day = day
    return max_day


def max_expenses(expenses, command_param, _history_list):
    '''
    Displays the day with the maximum expenses
    :param expenses: list of expenses (type: list)
    :param command_param: the word "day" (type: list)
    :param _history_list: the history list (type: list)
    :return: Nothing
    '''
    if not command_param[0] == 'day' or not len(command_param) == 1:
        raise ValueError('Wrong input or too many parameters!')
    maxx(expenses)
    max_day = maxx(expenses)
    print_max_day(max_day)


def get_sort_list_day(expenses):
    '''
    Display the total daily expenses in ascending order by money
    :param expenses: the list of expenses (type: list)
    :return: the sorted list (type: list)
    '''
    a = sorted(expenses, key=lambda i: i["amount_of_money"])
    return a


def get_sort_list_category(expenses, category):
    '''
    Display the total daily expenses in ascending order by a certain category
    :param expenses: the list of expenses (type: list)
    :param category: the category (type: string)
    :return: the sorted list (type: list)
    '''
    key_val_list = [category]
    category_list = list(filter(lambda d: d["expense_type"] in key_val_list, expenses))
    b = sorted(category_list, key=lambda i: i["amount_of_money"])
    return b


def sort_expenses(_expenses, command_param, _history_list):
    '''
    Display the total daily expenses in ascending order by amount of money spent or by category
    :param _expenses:
    :param command_param:
    :param _history_list: the history list (type: list)
    :return: Nothing
    '''
    if len(command_param) == 1:
        if command_param[0] == 'day':
            a = get_sort_list_day(_history_list[len(_history_list)-1])
            display_list(a)
        elif check_type(command_param[0]) == 'string':
            b = get_sort_list_category(_history_list[len(_history_list)-1], command_param[0])
            display_list(b)
        else:
            raise ValueError("Wrong parameter!")
    else:
        raise ValueError("Too many parameters!")


# ---- filter expenses ----


def f_what_command(command_param):
    '''
    -We check if the parameters for the filter function are correct.
    -If they are, we find out what command the user wants (from the 4 available commands)
    :param command_param: list of parameters (type: list)
    :return: the number of the command (type: int)
    '''
    if len(command_param) == 1 and check_type(command_param[0]) == 'string':
        return 1
    if len(command_param) == 3 and check_type(command_param[0]) == 'string' and\
            check_type(command_param[2]) == 'natural':
        if command_param[1] == '<':
            return 2
        elif command_param[1] == '=':
            return 3
        elif command_param[1] == '>':
            return 4
        else:
            raise ValueError("Choose from <,=,>")
    else:
        raise ValueError("Wrong input! See the available options:"
                         "\n\tlist\n\tlist <category>"
                         "\n\tlist <category> [ < | = | > ] <value>")


def filterr(p, expenses, command_param):
    '''
        We display the list of expenses based on the chosen option
        :param p:
        - for p=2 -> we use '<'
        - for p=3 -> we use '='
        - for p=4 -> we use '>'
        :param expenses: list of expenses (type: list)
        :param command_param: the parameters (type: list)
        :return: Nothing
    '''
    key_val_list = [command_param[0]]
    category_list = list(filter(lambda d: d["expense_type"] in key_val_list, expenses))
    if p == 1:
        return category_list
    elif p == 2:
        value = int(command_param[2])
        final_list = list(filter(lambda d: int(d["amount_of_money"]) < value, category_list))
        return final_list
    elif p == 3:
        value = int(command_param[2])
        final_list = list(filter(lambda d: int(d["amount_of_money"]) == value, category_list))
        return final_list
    elif p == 4:
        value = int(command_param[2])
        final_list = list(filter(lambda d: int(d["amount_of_money"]) > value, category_list))
        return final_list


def filter_expenses(expenses, command_param, history_list):
    '''
    We display the list of expenses based on the chosen option
    :param expenses: list of expenses (type: list)
    :param command_param: the parameters (type: list)
    :param history_list: the history list (type: list)
    :return: Nothing
    '''
    p = f_what_command(command_param)
    expenses = filterr(p, expenses, command_param)
    ex_copy = deepcopy(expenses)
    history_list.append(ex_copy)
    print(expenses)
    display_by_category2(expenses)


def undo(history_list):
    '''
    We undo the last change
    :param history_list: the history list
    :return: nothing
    '''
    length = len(history_list)
    if length == 1:
        print("No more undo!")
        return 'no_more'
    else:
        history_list.pop(length-1)
        expenses = history_list[length-2].copy()
        return expenses


# ---- other ---
def split_command(command):
    '''
    It splits the command into multiple words and it transforms them into lower cases
    :param command: what it was inserted (type: string)
    :return: the command word and parameters (type: string and list)
    '''
    tokens = command.strip().split()
    command_word = tokens[0].lower()
    command_param = []
    for i in range(len(tokens)-1):
        command_param.append(tokens[i+1].lower())
    return command_word, command_param

# ----- tests -----


def test_init(expenses_list):
    '''
    Include at least 10 items in the application at startup
    :param expenses_list: the list of expenses (type: list)
    :return: Nothing
    '''
    expenses_list.append(create_expense(3, 100, 'internet'))
    expenses_list.append(create_expense(3, 50, 'others'))
    expenses_list.append(create_expense(4, 50, 'others'))
    expenses_list.append(create_expense(10, 50, 'others'))
    expenses_list.append(create_expense(20, 1000, 'housekeeping'))
    expenses_list.append(create_expense(5, 44, 'transport'))
    expenses_list.append(create_expense(7, 350, 'clothing'))
    expenses_list.append(create_expense(4, 100, 'food'))
    expenses_list.append(create_expense(10, 50, 'food'))
    expenses_list.append(create_expense(20, 500, 'transport'))


def test_create_expense():
    '''
    We test the create function
    :return: Nothing
    '''
    try:
        create_expense(-3, 67, 'food')
        assert False
    except ValueError:
        pass

    try:
        create_expense(4.5, 67, 'food')
        assert False
    except ValueError:
        pass

    try:
        create_expense(35, 67, 'food')
        assert False
    except ValueError:
        pass

    try:
        create_expense(20, 55, 'greh')
        assert False
    except ValueError:
        pass


def test_modify(expenses, history_list):
    '''
    We test the modify function
    :param expenses:
    :return: Nothing
    '''
    try:
        modify_expenses(expenses, [-3, 'to', 10], history_list)
        assert False
    except ValueError:
        pass

    try:
        modify_expenses(expenses, [3, 'to', 10], history_list)
        assert True
    except ValueError:
        pass


def test_display(expenses):
    '''
    Test display function
    :param expenses:
    :return:
    '''
    # ---- display_expenses(expenses, ['food']) ----
    list_expected1 = [{'day': 4, 'amount_of_money': 100, 'expense_type': 'food'},
                      {'day': 10, 'amount_of_money': 50, 'expense_type': 'food'}]
    actual_expenses1 = []
    for i in range(1, 31):
        for j in range(len(expenses)):
            if get_day(expenses[j]) == i and get_type(expenses[j]) == 'food':
                actual_expenses1.append(expenses[j])
    assert list_expected1 == actual_expenses1

    # ---- display_expenses(expenses, ['others', '=' , 50]) ----
    list_expected2 = [{'day': 3, 'amount_of_money': 50, 'expense_type': 'others'},
                      {'day': 4, 'amount_of_money': 50, 'expense_type': 'others'},
                      {'day': 10, 'amount_of_money': 50, 'expense_type': 'others'}]
    actual_expenses2 = []
    for i in range(1, 31):
        for j in range(len(expenses)):
            if get_day(expenses[j]) == i and get_type(expenses[j]) == 'others':
                if get_money(expenses[j]) == 50:
                    actual_expenses2.append(expenses[j])
    assert list_expected2 == actual_expenses2


def test_sum(expenses):
    '''
    Test the sum function
    :param expenses: list of expenses
    :return: nothing
    '''
    # sum food
    expected_result = 150
    actual_result = summ(expenses, 'food')
    assert expected_result == actual_result

    # sum housekeeping
    expected_result = 1000
    actual_result = summ(expenses, 'housekeeping')
    assert expected_result == actual_result


def test_max(expenses):
    '''
    Test max function
    :param expenses: list of expenses
    :return: Nothing
    '''
    # max day
    expected_result = 20
    actual_result = maxx(expenses)
    assert expected_result == actual_result


def test_sort():
    '''
    The sort functiob
    :return: Nothing
    '''
    # sort food
    example_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'internet'}]
    expected_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                     {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'}]

    actual_list = get_sort_list_category(example_list, 'food')
    assert expected_list == actual_list

    # sort day
    example_list = [{'day': 4, 'amount_of_money': 100, 'expense_type': 'internet'},
                    {'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'}, ]
    expected_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                     {'day': 4, 'amount_of_money': 100, 'expense_type': 'internet'},
                     {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'}]
    actual_list = get_sort_list_day(example_list)
    assert expected_list == actual_list


def test_filter():
    '''
    Test filter function
    :return: Nothing
    '''
    # filter food
    example_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'internet'}]
    expected_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                     {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'}]

    actual_list = filterr(1, example_list, ['food'])
    assert expected_list == actual_list

    # filter food < 60
    example_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'internet'}]
    expected_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'}]

    actual_list = filterr(2, example_list, ['food', '<', 60])
    assert expected_list == actual_list


def test_undo():
    '''
    Test undo function
    :return: Nothing
    '''
    example_list = [{'day': 10, 'amount_of_money': 50, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'food'},
                    {'day': 4, 'amount_of_money': 100, 'expense_type': 'internet'}]
    history_list = list()
    ex_copy = deepcopy(example_list)
    history_list.append(ex_copy)
    add_new_expense(example_list, [100, 'food'], history_list)
    ex_copy = deepcopy(example_list)
    history_list.append(ex_copy)
    expected_list = undo(history_list)
    assert expected_list == example_list
