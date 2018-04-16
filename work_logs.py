from csv_functions import clear_all_logs, initialize_work_log
from log import Log
from search import Search
from user_navigation_functions import clear_screen, menu


def greet_user():
    '''Greet the user'''
    clear_screen()
    input("Hello, welcome to the work log program. Press any key to continue")


def goodbye():
    '''Say goodbye when the program ends'''
    clear_screen()
    print("Thank you for using the work log program!")
                

def work_logs_program():
    main_options = {
        '1': 'Log Work',
        '2': 'Search Logs',
        '3': 'Clear All Logs',
        '4': 'Quit'
    }
    # Build the work_log.txt file if non exists
    initialize_work_log()
    
    # Get user's choice from the main menu options
    while True:
        clear_screen()
        print("Main Menu")
        nav = menu(main_options)

        if nav == 'Log Work':
            new_log = Log()
            new_log.create_new_log()
            
        if nav == 'Search Logs':
            search_log_loop()
            
        if nav == 'Clear All Logs':
            clear_all_logs()
            
        if nav == 'Quit':
            break


def search_log_loop():
    search_options = {
        '1': 'Search by Date',
        '2': 'Search by Date Range',
        '3': 'Search by Work Time Spent',
        '4': 'Search by Word or Phrase',
        '5': 'Search by Pattern (Regex)',
        '6': 'Return to Main Menu'
    }
    while True:
        
        # Fetch a list of the logs from work_log.txt.
        clear_screen()
        
        # Present the search menu and get the user's choice.
        print("Search Menu")
        nav = menu(search_options)
        clear_screen()

        # Break search loop if return to main menu is chosen.
        if nav == 'Return to Main Menu':
            break

        # Otherwise execute the chosen search option.
        else:
            search = Search()
            if nav == 'Search by Date':
                search.search_by_date()
                
            if nav == 'Search by Date Range':
                search.search_by_date_range()
                
            if nav == 'Search by Work Time Spent':
                search.search_by_time_spent()
                
            if nav == 'Search by Word or Phrase':
                search.search_by_string()
                
            if nav == 'Search by Pattern (Regex)':
                search.search_by_pattern()

            search.detail_view()


if __name__ == '__main__':
    greet_user()
    
    work_logs_program()
    
    goodbye()
    

