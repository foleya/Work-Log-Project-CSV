import os


def confirm_user_action():
    '''
    Confirms a user's action
    
    Prompt the user for confirmation for an action (like edit, delete, or clear
    all logs).
    
    Arguments: None
    Returns: Boolean (True/Confirmation or False/Disconfirmation)
    '''
    confirm = input("Confirm this action (y/N)").lower()
    if confirm != 'y':
        input("\nChange discarded. Press any key to continue.")
        return False
    else:
        input("\nChange confirmed. Press any key to continue.")
        return True


def clear_screen():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu(options):
    '''
    Displays a menu and returns user's choice
    
    Using a dictionary of keys (numbers as strings) and values (options as
    strings)--e.g. {'1', 'Add Log', '2': 'Quit'}, this displays a menu and then
    prompts the user to make a selection from the available options. The
    function will not return a selection until the user has chosen a valid
    option from the menu.
    
    Argument: Dictionary (With numbers and options: e.g. {'1': 'Quit'})
    Returns: String (Value from dictionary (i.e. an option from the menu))
    '''
    for number, option in options.items():
        print("{}: {}".format(number, option))
    print("\n")

    while True:
        nav = input("Choose an option (1-{}): ".format(len(options)))
        try:
            options[nav]
        except KeyError:
            print(
                "\nSorry, '{}' is not a valid option. "
                "Please choose a number 1-{}.\n".format(nav, len(options))
            )
        else:
            break

    return options[nav]


