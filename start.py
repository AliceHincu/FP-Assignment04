"""
Assemble the program and start the user interface here
"""
from functions.functions import add_new_expense, display_expenses, modify_expenses, insert_new_expense, \
    split_command, sum_expenses, max_expenses, sort_expenses, filter_expenses, undo, test_init, test_sum, test_max, \
    test_sort, test_filter, test_undo, test_display, test_create_expense
from ui.console import print_error, print_menu, print_goodbye, print_bad_command


def tests(expenses):
    '''
    We test the functions
    :param expenses: list of expenses
    :return: nothing
    '''
    test_create_expense()
    test_display(expenses)
    test_sum(expenses)
    test_max(expenses)
    test_sort()
    test_filter()
    test_undo()


if __name__ == '__main__':
    print_menu()
    expenses = []
    history_list = []
    test_init(expenses)
    ex_copy = expenses[:]
    history_list.append(ex_copy)
    tests(expenses)
    command_dict = {'add': add_new_expense, 'insert': insert_new_expense,
                    'remove': modify_expenses, 'list': display_expenses,
                    'sum': sum_expenses, 'max': max_expenses,
                    'sort': sort_expenses, 'filter': filter_expenses}
    done = False

    while not done:
        command = input('\ncommand> ')
        command_word, command_param = split_command(command)

        if command_word in command_dict:
            try:
                command_dict[command_word](expenses, command_param, history_list)
            except ValueError as val_error:
                print_error(val_error)
        elif command_word == 'exit':
            done = True
            print_goodbye()
        elif command_word == 'undo':
            undo_list = undo(history_list)
            if not undo_list == 'no_more':
                expenses = undo_list
        else:
            print_bad_command()
