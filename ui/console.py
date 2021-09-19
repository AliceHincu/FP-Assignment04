"""
This is the user interface module. These functions call functions from the domain and functions module.
"""

import tabulate
from termcolor import colored


# ---- UI functions ----


def display_by_days2(expenses):
    '''
    Displays by days (p1)
    :param expenses: list of expenses( type: list)
    :return: Nothing
    '''
    headers = expenses[0].keys()
    rows = [expense.values() for expense in expenses]
    print(tabulate.tabulate(rows, headers, tablefmt='grid'))


def display_by_category2(expenses):
    '''
        Displays by category (p2)
        :param expenses: list of expenses( type: list)
        :return: Nothing
        '''
    if len(expenses) == 0:
        print("The list is empty!")
    else:
        headers = expenses[0].keys()
        rows = [expense.values() for expense in expenses]
        print(tabulate.tabulate(rows, headers, tablefmt='grid'))


def display_list(expenses):
    '''
    Displays the list
    :param expenses: the list of expenses
    :return: nothing
    '''
    headers = expenses[0].keys()
    rows = [expense.values() for expense in expenses]
    print(tabulate.tabulate(rows, headers, tablefmt='grid'))


def display_none(category):
    '''
    If nothing needs to be displayed
    :return: Nothing
    '''
    print("\tThere are no expenses for " + str(category) + "in this month yet.")


def display_by_category_compare2(expenses):
    '''
        Displays by days (p1)
        :param expenses: list of expenses( type: list)
        :return: Nothing
        '''
    headers = expenses[0].keys()
    rows = [expense.values() for expense in expenses]
    print(tabulate.tabulate(rows, headers, tablefmt='grid'))


def display_none2(p, category, value):
    '''
    If nothing needs to be displayed
    :param p : if it needs to be <,=,>
    :param category: from what category
    :param value :the value to compare
    :return : Nothing
    '''
    if p == 3:
        print("\tThere are no expenses for the category -" + str(category) +
              "- which are smaller than " + str(value) + " RON in this month yet.")
    elif p == 4:
        print("\tThere are no expenses for the category -" + str(category) +
              "- which are equal to " + str(value) + " RON in this month yet.")
    else:
        print("\tThere are no expenses for the category -" + str(category) +
              "- which are greater than " + str(value) + " RON in this month yet.")


def print_menu():
    '''
    Prints the menu with the commands
    :return: Nothing
    '''
    print("\n(A) Add a new expense")
    print("\t\tadd <sum> <category>\n\t\tinsert <day> <sum> <category>")
    print("(B) Modify expenses")
    print("\t\tremove <day>\n\t\tremove <start day> to <end day>\n\t\tremove <category>")
    print("(C) Display expenses with different properties")
    print("\t\tlist\n\t\tlist <category>\n\t\tlist <category> [ < | = | > ] <value>. Condition:"
          "the value has to be a positive natural number")
    print("(D) Obtain different characteristics of sublist")
    print("\t\tsum <category>\n\t\tmax day\n\t\tsort day\n\t\tsort <category>")
    print("(E) Filter expenses")
    print("\t\tfilter <category>\n\t\tfilter <category> [ < | = | > ] <value>")
    print("(F) Undo")
    print("\t\tundo")


def print_goodbye():
    '''
    A goodbye message
    :return: Nothing
    '''
    print('Goodbye! ^_^')


def print_bad_command():
    '''
    Called when the command that was written isn't good
    :return: Nothing
    '''
    print('Oops ... bad command! Please try again!')


def print_error(error):
    '''
    Prints the customized text for the error
    :param error: the text of the error
    :return: Nothing
    '''
    print(str(error))


def print_sum(sum, category):
    '''
    Displays the total expense for a certain category
    :param sum: the total sum (type: int)
    :param category: the category (type: string)
    :return:
    '''
    print("The total expense for the category " + str(category) + " is: " + colored(str(sum), 'red') + " RON")


def print_max_day(day):
    '''

    :param day:
    :return:
    '''
    print("The day with the maximum expenses is: day " + colored(str(day), 'red'))
