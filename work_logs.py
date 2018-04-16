import datetime
import csv
import os
import re
import sys


def clear_screen():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def greet_user():
    '''Greet the user'''
    clear_screen()
    input("Hello, welcome to the work log program. Press any key to continue")


def goodbye():
    '''Say goodbye when the program ends'''
    clear_screen()
    print("Thank you for using the work log program!")


def initialize_work_log():
    '''
    Checks to make sure work_log.txt exists and has the appropriate headers
    '''
    try:
        log = open("work_log.txt")
        log.close()
        
    # If no work_log.txt, create file with appropriate headers.
    except FileNotFoundError:
        with open("work_log.txt", "w+") as work_log:
            work_log.write('date,title,duration,note\n')
        return True

    # If pre_existing work_log.txt uses wrong (or no) headers, exit the program
    # while prompting the user to fix the headers.
    else:
        with open("work_log.txt", "r") as work_log:
            if work_log.readline() != 'date,title,duration,note\n':
                clear_screen()
                print(
                    "Oh no! It looks like the header in work_log.txt "
                    "is not formatted properly.\n\nMake sure the first "
                    "line of work_log.txt is 'date,title,duration,note', "
                    "then try opening the program again."
                )
                sys.exit()
            else:
                pass


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


def get_valid_date_format():
    '''
    Prompts the user to enter a date with format DD/MM/YYYY
    
    This prompts the user to enter a date, ensuring that the date entered
    has the proper format: DD/MM/YYYY. This is important for ensuring
    consistent date formats in the work_log.txt file.
    
    Arguments: None
    Returns: String (Date with format DD/MM/YYYY)
    '''
    while True:
        date = input('(DD/MM/YYYY): ')
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
        except:
            print(
                "\n"
                "--- Sorry, '{}' is not a valid date format. "
                "Please use DD/MM/YYYY. ---"
                "\n".format(date)
            )
        else:
            break
    return date


def get_log_date():
    '''
    Returns user input of the date of a work log
    
    Prompts the user to enter the date of a work log. Uses
    get_valid_date_format() to ensure the date has the proper format:
    DD/MM/YYYY.
    
    Arguments: None
    Returns: String (Date of work log with format DD/MM/YYYY)
    '''
    print("Enter the date of this work.")
    return get_valid_date_format()


def get_log_title():
    '''
    Returns user input of the title of a work log
    
    Prompts the user to enter a note and checks to make sure only normal
    alphanumeric and punctuation characters were entered, and that the
    entire field is not surrounded by doublequotes, helping ensure that
    fetch_logs() will not have an issue fetching notes.
    
    Arguments: None
    Returns: String (Title of a work log)
    '''
    while True:
        title = input('Enter a title for this work: ')
        if title == '':
            print("Please enter a title.")
        elif re.match(r'^[-\w\d\s.!\(\);:,\'?]+$', title):
            break
        else:
            print(
                "---\nSorry! Invalid characters detected. Please stick to "
                "using alphanumerics and normal punctuation. Try again!---\n"
            )
    return title


def get_log_duration():
    '''
    Returns user input of the duration of a work log
    
    Prompts the user to enter a duration of a piece of work and checks to make
    sure only a whole number was entered.
    
    Arguments: None
    Returns: String (Number of minutes rounded of a work log)
    '''
    while True:
        duration = input('Enter how many minutes you worked (rounded): ')
        try:
            int(duration)
        except ValueError:
            print(
                "\n"
                "--- Sorry, '{}' is not a whole number. "
                "Please enter a whole number. ---"
                "\n".format(duration)
            )
        else:
            break
    return duration


def get_log_note():
    '''
    Returns user input of the note of a work log
    
    Prompts the user to enter a note and checks to make sure only normal
    alphanumeric and punctuation characters were entered, and that the
    entire field is not surrounded by doublequotes, helping ensure that
    fetch_logs() will not have an issue fetching notes.
    
    Arguments: None
    Returns: String (Note for a work log)
    '''
    while True:
        note = input("Enter an (optional) note about this work: ")
        if note[0] == '"' and note[-1] == '"':
            print(
                "\n---Sorry! The note field cannot be surrounded by "
                "doublequotes. Try again.---\n"
            )
        elif not re.match(r'^[-\w\d\s.,!\(\);:\'"?]+$', note):
            print(
                "---\nSorry! Invalid characters detected. Please stick to "
                "using alphanumerics and normal punctuation. Try again!---\n"
            )
        elif note == '':
            note = 'None'
            break
        else:
            break
  
    return note


def get_log_details():
    '''
    Gets all the details for a work log
    
    Using get_log_date(), get_log_title(), get_log_duration(), and
    get_log_note(), this asks the user to input the date, title, duration of a
    work log, as well as an optional note.
    
    Arguments: None
    Returns: Four Strings (date, title, duration, and note)
    '''
    date = get_log_date()
    title = get_log_title()
    duration = get_log_duration()
    note = get_log_note()
    return date, title, duration, note


def add_log(date, title, duration, note):
    '''
    Appends a work log to work_log.txt
    
    Takes the date, title, duration, and note for a work log and writes
    those values to a csv file. Commas are used as delimeters.
    
    Arguments: 4 Strings (date, title, duration, note)
    Returns: Nothing (just writes a new work log to a file)
    '''
    with open('work_log.txt', 'a+', newline='') as work_log:
        logwriter = csv.writer(
            work_log,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )
        logwriter.writerow([date] + [title] + [duration] + [note])


def create_new_log():
    '''
    Prompts user for new log details then adds them to work_log.txt
    
    Using get_log_details() this gets the date, title, duration, and an
    optional note. Then using add_log() it appends those details to
    work_log.txt.
    
    Arguments: None
    Returns: Nothing (just prompts for details and writes them to a file)
    '''
    clear_screen()
    new_log = get_log_details()
    add_log(*new_log)

    clear_screen()
    print("New work log created:")
    display_log(*new_log)

    input("\nHit 'Enter' to return to the Main Menu.")


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


def delete_log(date, title, duration, note):
    '''
    Deletes a log from work_log.txt
    
    This rewrites the work_log.txt file, excluding a specific log the user
    has chosen to delete. To do this, first, all the logs from fetch_logs() are
    given their line numbers in the csv (with enumerate). Then the log to be
    deleted is matched with its line number, allowing the file to be
    rewritten, with the exclusion of the line number associated with the
    log to be deleted.
    
    Arguments: 4 Strings (Date, title, duration, and note for a work log)
    Returns: Nothing (just deletes a log from work_log.txt)
    '''
    # Create a list of logs matched with their line numbers.
    logs_with_line_numbers = list(enumerate(fetch_logs(), 1))
    
    # For any log in that list, if it has details that match the log scheduled
    # for deletion, add its line number to a list of line numbers to be
    # deleted.
    line_numbers_to_delete = []
    for num, log in logs_with_line_numbers:
        if {
            'date': date,
            'title': title,
            'duration': duration,
            'note': note
        } == log:
            line_numbers_to_delete.append(num)
    
    # Re-write the work_logs.txt file, excluding any lines with line_numbers
    # that were scheduled for deletion. Setting the header line to '0', and
    # generating line numbers with enumerate again.
    with open("work_log.txt", "r+") as work_log:
        data = work_log.readlines()
        work_log.seek(0)
        for line_num, line in enumerate(data, 0):
            if line_num not in line_numbers_to_delete:
                work_log.write(line)
        work_log.truncate()


def edit_log(date, title, duration, note):
    '''
    Prompts a user to edit the date, title, duration, and/or note for a log
    
    Using a dictionary of options to generate a menu, this asks whether the
    user would like to edit the date, title, duration, and/or note for a work
    log. The desired fields are retrieved, then a new log with the editted and
    original fields (if any) is appended to work_log.txt -- while the original
    log is deleted from work_log.txt
    
    Argument: 4 Strings (date, title, duration, and note for log to be editted)
    Returns: Nothing (just updates work_log.txt with the edits)
    '''
    edit_options = {
        '1': 'Date',
        '2': 'Title',
        '3': 'Duration',
        '4': 'Note',
        '5': 'All Fields',
        '6': 'No Fields (Return to Search Menu)'
    }
    # Display the log the user desires to edit and present them with the edit
    # menu, getting their chosen action.
    original_log = (date, title, duration, note)
    clear_screen()
    print("Original Log:")
    display_log(*original_log)
    print("\nWhat field(s) would you like to edit?")
    edit_field = menu(edit_options)

    # Return the user to the search menu if no edits are desired.
    if edit_field == 'No Fields (Return to Search Menu)':
        pass

    # Generate an editted version of the original log, based on which fields
    # the user chose to edit.
    else:
        if edit_field == 'Date':
            edit = get_log_date()
            editted_log = (edit, title, duration, note)

        if edit_field == 'Title':
            edit = get_log_title()
            editted_log = (date, edit, duration, note)

        if edit_field == 'Duration':
            edit = get_log_duration()
            editted_log = (date, title, edit, note)

        if edit_field == 'Note':
            edit = get_log_note()
            editted_log = (date, title, duration, edit)

        if edit_field == 'All Fields':
            editted_log = get_log_details()

    # Display the original and editted logs to the user.
        clear_screen()
        display_log(*original_log)
        print("\n--- Will Be Replaced With---\n")
        display_log(*editted_log)

    # Update work_log.txt if the user confirms their edits by adding the
    # editted log, and deleting the original log.
        if confirm_user_action():
            add_log(*editted_log)
            delete_log(*original_log)


def clear_all_logs():
    '''Clears/Deletes all work logs'''
    confirm = input("Enter 'CLEAR' to clear all logs.").lower()

    if confirm == 'clear':
        with open('work_log.txt', 'w+') as work_log:
            work_log.write('date,title,duration,note\n')
        input(
            "All work logs have been cleared. "
            "Hit 'Enter' to return to the Main Menu."
        )

    else:
        input(
            "Work logs have been preserved. "
            "Hit 'Enter' to return to the Main Menu."
        )


def display_log(date, title, duration, note):
    '''
    Displays a work log
    
    Uses the date, title, duration, and optional note for a work log to display
    a formatted string to the user.
    
    Arguments: Four Strings (Date, title, duration, and note for a work log)
    Returns: Nothing (Just prints a formatted string)
    '''
    print(
        "Date: {d}\n"
        "Title: {t}\n"
        "Duration: {m} Minutes\n"
        "Note: {n}\n".format(d=date, t=title, m=duration, n=note)
    )
    

def search_by_date(logs):
    '''
    Searches for work logs by their date
    
    Using a list of logs--which are dictionaries retrieved by fetch_logs()--
    this creates a list of unique log-dates to generate a menu of date options.
    Once the user has chosen a date from that menu, this builds a list of logs
    that have that date.
    
    Argument: List of dictionaries (Logs grabbed by fetch_logs())
    Returns: List of dictionaries (Logs with chosen date)
    '''
    # Get a list of unique dates from the fetched logs.
    dates = []
    for log in logs:
        if log['date'] not in dates:
            dates.append(log['date'])

    # Build a dictionary of options and have menu() display them to the user.
    # Then set date_choice to the user's date-menu selection.
    if dates:
        x = 1
        date_options = {}
        for date in dates:
            date_options[str(x)] = date
            x += 1
        print("Choose a date to see its logs:")
        date_choice = menu(date_options)
    
    # If there are no dates (because work_log.txt was
    # empty or nonexistant and thus fetch_logs returned nothing), sets
    # the date choice to None, which will return no search results.
    else:
        date_choice = None

    # Return a list of logs that have the same date as the user's date_choice.
    search_results = []
    for log in logs:
        if log['date'] == date_choice:
            search_results.append(log)
    return search_results


def search_by_date_range(logs):
    '''
    Searches for work logs by dates within a specified range
    
    After asking the user to input a start and end date, and parsing those
    inputs into datetime objects. This searches a list of logs -- which are
    dictionaries grabbed by fetch_logs() -- for logs that fall between
    the specified dates.
    
    The range check is done by calculating the maximum range (end date - start
    date), then checking to see if the difference between the end date and each
    log's date falls between 0 and the maximum range (i.e. the log's date is
    not after the end date or before the start date).
    
    Argument: List of dictionaries (Logs grabbed by fetch_logs())
    Returns: List of dictionaries (Logs in chosen date range)
    '''
    # Ask user to input a start and end date, then parse that input to create
    # datetime objects.
    print("Enter the start date for your range search.")
    start_date = get_valid_date_format()
    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    print("Enter the end date for your range search.")
    end_date = get_valid_date_format()
    end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
    
    # Create a timedelta with a value of 0 (for the range's minimum) and
    # calculate a timedelta that represents the maximum value allowed
    # by the search (end_date - start_date)
    range_start = datetime.timedelta(0)
    range_max = end_date - start_date

    # Return a list of logs that have dates falling within the search range.
    search_results = []
    for log in logs:
        date = end_date - datetime.datetime.strptime(log['date'], '%d/%m/%Y')
        if date >= range_start and date <= range_max:
            search_results.append(log)
    return search_results


def search_by_duration(logs):
    '''
    Searches for work logs with a specified duration
    
    Prompts the user for the duration of a piece of work in rounded minutes,
    then, after ensuring the user has input whole numbers, searches the logs
    -- which are a list of dictionaries grabbed by fetch_logs() -- and builds
    a list of logs that have the specified duration.
    
    Argument: List of dictionaries (grabbed by fetch_logs())
    Returns: List of dictionaries (logs with specified duration)
    '''
    # Prompt user to enter a duration, ensuring the user enters a whole number.
    while True:
        duration_choice = input(
            "Enter the duration you'd like to search for "
            "(in rounded minutes):"
            )
        try:
            int(duration_choice)
        except ValueError:
            print(
                "\n--- Sorry, '{}' is not a whole number. "
                "Please enter a whole number. ---"
                "\n".format(duration_choice)
            )
        else:
            break
    
    # Return a list of logs that have the specified duration
    search_results = []
    for log in logs:
        if log['duration'] == duration_choice:
            search_results.append(log)
    return search_results


def search_by_string(logs):
    '''
    Searches the work logs for a specific string of characters
    
    Prompts the user to enter a string of characters, then using re.match,
    searches the logs -- which are a list of dictionaries grabbed by fetch_logs
    -- for logs with titles or notes that contain the specified string.
    re.Ignorecase is used to allow more flexibility in terms of searching.
    
    Argument: List of dictionaries (grabbed by fetch_logs)
    Returns: List of dictioanries (logs containing the specified string)
    '''
    # Ask user to input a string.
    s = input(
        "Please enter the word or phrase you'd like to search for: "
    )

    # Return a list of logs that have titles or notes containing the specified
    # string.
    search_results = []
    for log in logs:
        if re.search(s, log['title'], re.I) or re.search(s, log['note'], re.I):
            search_results.append(log)
    return search_results


def search_by_pattern(logs):
    '''
    Searches the work logs for a specific pattern of characters
    
    Prompts the user to enter a Regex pattern, using re.compile to ensure that
    valid regex syntax has been used. Then using re.match, searches the logs
    -- which are a list of dictionaries grabbed by fetch_logs() -- and builds
    a list of logs that have title and/or note fields that match the specified
    pattern.
    
    Argument: List of dictionaries (grabbed by fetch_logs)
    Returns: List of dictioanries (logs containing the specified pattern)
    '''
    # Ask user to input a regex pattern, check to make sure it can be compiled.
    while True:
        pattern = input(
            "Please enter the pattern (regular expression) "
            "you'd like to search for: "
        )
        try:
            regex = re.compile(pattern)
        except:
            print("\n---Invalid Regex Syntax. Please try again.---")
        else:
            break

    # Return a list of logs with titles and/or notes that match that specified
    # pattern.
    search_results = []
    for log in logs:
        if regex.search(log['title']) or regex.search(log['note']):
            search_results.append(log)
    return search_results


def fetch_logs():
    '''
    Reads a csv and returns all logs (as a list of dictionaries)
    
    Using csv.DictReader(), work_log.txt is read and dictionaries
    corresponding to each line in the file are added to a list.
    
    Argument: None
    Returns: List of Dictionaries (all logs in work_log.txt)
    '''
    logs = []

    with open("work_log.txt", newline='') as work_log:
        reader = csv.DictReader(work_log, quotechar='|')
        for row in reader:
            logs.append(row)

    return logs


def sorting(logs):
    '''Defines a sorting key to be used by fetch_sorted_logs()'''
    splitup = logs['date'].split('/')
    return splitup[2], splitup[1], splitup[0]


def fetch_sorted_logs(logs):
    '''Sorts a list of logs by their dates using sorting() as a key'''
    return sorted(logs, key=sorting)


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
            create_new_log()
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
        '3': 'Search by Work Duration',
        '4': 'Search by Word or Phrase',
        '5': 'Search by Pattern (Regex)',
        '6': 'Return to Main Menu'
    }
    while True:
        
        # Fetch a list of the logs from work_log.txt.
        clear_screen()
        logs = fetch_logs()
        
        # Present the search menu and get the user's choice.
        print("Search Menu")
        nav = menu(search_options)
        clear_screen()

        # Break search loop if return to main menu is chosen.
        if nav == 'Return to Main Menu':
            break

        # Otherwise execute the chosen search option.
        else:
            if nav == 'Search by Date':
                search_results = search_by_date(fetch_sorted_logs(logs))
            if nav == 'Search by Date Range':
                search_results = search_by_date_range(logs)
            if nav == 'Search by Work Duration':
                search_results = search_by_duration(logs)
            if nav == 'Search by Word or Phrase':
                search_results = search_by_string(logs)
            if nav == 'Search by Pattern (Regex)':
                search_results = search_by_pattern(logs)

            detail_view(search_results)


def detail_view(search_results):
    clear_screen()
    
    # If the search yielded results, display the first result and set an index
    # to 0, which will be used for paging through the results.
    if search_results:
        index = 0
        while True:
            print(
                "Displaying result "
                "{} of {}".format(index + 1, len(search_results))
            )
            try:
                display_log(**search_results[index])
            except TypeError:
                input(
                    "Oh no! It looks like the data in work_logs.txt is not "
                    "formatted correctly!\nPress any key to return to the "
                    "Search Menu."
                )
                break
            
            # Display navigation options for the search result detail view.
            nav = input(
                "[N]ext, [P]revious, [E]dit, [D]elete, "
                "[R]eturn to Search Menu: "
            ).lower()

            # Page to next result (if any)
            if nav == 'n' and index != len(search_results) - 1:
                index += 1
                
            # Page to previous result (if any)
            if nav == 'p' and index != 0:
                index -= 1
            
            # Enter edit log dialogue.
            if nav == 'e':
                edit_log(**search_results[index])
                break
            
            # Enter delete log dialogue.
            if nav == 'd':
                if confirm_user_action():
                    delete_log(**search_results[index])
                break
            
            # Break search result detail view loop if [R]eturn is selected.
            if nav == 'r':
                break
                
            # Keep loop going if navigation input is invalid.
            else:
                clear_screen()
                continue
    
    # If no search results, announce that and leave search result detail view.
    else:
        nav = input(
            "---Sorry, no results matched your search.---"
            "\nPress any key to return to the Search Menu."
        )
        pass


if __name__ == '__main__':
    greet_user()
    
    work_logs_program()
    
    goodbye()
    

