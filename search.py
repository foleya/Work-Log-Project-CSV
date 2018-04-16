import datetime
import re

from csv_functions import fetch_logs
from user_input_functions import get_valid_date_format, get_valid_time_spent
from user_navigation_functions import clear_screen, confirm_user_action, menu
from log import Log


def sorting(logs):
    '''
    Defines a sorting key to be used by the Search class's __init__ method
    
    Looks through a list of logs grabbed by fetch_logs(), splits each log's
    date by year, month, date into a key for sorted() to then use for
    chronological sorting of the logs.
    
    Argument: List of dictionaries (logs grabbed by fetch_logs())
    Returns: Sorting Key (year, month, day)
    '''
    splitup = logs['date'].split('/')
    return splitup[2], splitup[1], splitup[0]


class Search():
    
    def __init__(self):
        '''Get a chronologically sorted list of logs from work_log.txt'''
        self.logs = sorted(fetch_logs(), key=sorting)
    
    def search_by_date(self):
        '''
        Searches for work logs by their date
    
        Using a list of logs--which are dictionaries retrieved by fetch_logs()
        -- this creates a list of unique log-dates to generate a menu of date
        options. Once the user has chosen a date from that menu, this searches
        the work logs for logs with that date, Updating self.search_results
        with any matches.
        '''
        # Sort logs by date (so that they can be displayed chronologically).
        
        # Get a list of unique dates from the fetched logs.
        dates = []
        for log in self.logs:
            if log['date'] not in dates:
                dates.append(log['date'])

        # Build a dictionary of options and have menu() display them to the
        # user. Then set date_choice to the user's date-menu selection.
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

        # Return a list of logs that have the same date as the user's
        # date_choice.
        self.search_results = []
        for log in self.logs:
            if log['date'] == date_choice:
                self.search_results.append(log)

    def search_by_date_range(self):
        '''
        Searches for work logs by dates within a specified range
    
        After asking the user to input a start and end date, and parsing those
        inputs into datetime objects. This searches a list of logs -- which are
        dictionaries grabbed by fetch_logs() -- for logs that fall between
        the specified dates.
    
        The range check is done by calculating the maximum range (end date -
        start date), then checking to see if the difference between the end
        date and each log's date falls between 0 and the maximum range (i.e.
        the log's date is not after the end date or before the start date).
        Updating self.search_results with any matches.
        '''
        # Ask user to input a start and end date, then parse that input to
        # create datetime objects.
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

        # Return a list of logs that have dates falling within the search
        # range.
        self.search_results = []
        for log in self.logs:
            date = end_date - datetime.datetime.strptime(
                log['date'], '%d/%m/%Y'
            )
            if date >= range_start and date <= range_max:
                self.search_results.append(log)

    def search_by_time_spent(self):
        '''
        Searches for work logs with a specified duration
    
        Prompts the user for the duration of a piece of work in rounded
        minutes, then, after ensuring the user has input whole numbers,
        searches the logs -- which are a list of dictionaries grabbed by
        fetch_logs() -- updating self.search_results with any matches.
        '''
        # Prompt user to enter a duration, ensuring the user enters a whole
        # number.
        time_spent_choice = get_valid_time_spent()
    
        # Return a list of logs that have the specified duration
        self.search_results = []
        for log in self.logs:
            if log['time_spent'] == time_spent_choice:
                self.search_results.append(log)

    def search_by_string(self):
        '''
        Searches the work logs for a specific string of characters
    
        Prompts the user to enter a string of characters, then using re.match,
        searches the logs -- which are a list of dictionaries grabbed by
        fetch_logs-- for logs with titles or notes that contain the specified
        string (re.Ignorecase is used to allow more flexibility in terms of
        searching). Updating self.search_results with any matches.
        '''
        # Ask user to input a string.
        ss = input(
            "Please enter the word or phrase you'd like to search for: "
        )

        # Return a list of logs that have titles or notes containing the
        # specified string.
        self.search_results = []
        for log in self.logs:
            if (re.search(ss, log['task_name'], re.I) or
                    re.search(ss, log['note'], re.I)):
                self.search_results.append(log)

    def search_by_pattern(self):
        '''
        Searches the work logs for a specific pattern of characters
    
        Prompts the user to enter a Regex pattern, using re.compile to ensure
        that valid regex syntax has been used. Then using re.match, searches
        the logs -- which are a list of dictionaries grabbed by fetch_logs() --
        updating self.search_results with any matches.
        '''
        # Ask user to input a regex pattern, check to make sure it can be
        # compiled.
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

        # Return a list of logs with titles and/or notes that match that
        # specified pattern.
        self.search_results = []
        for log in self.logs:
            if (regex.search(log['task_name']) or
                    regex.search(log['note'])):
                self.search_results.append(log)

    def detail_view(self):
        '''
        Displays logs in self.search_results
        
        Displays logs one at a time, allowing the user to page through all
        results, and potentially edit or delete a certain result.
        '''
        clear_screen()
        # If the search yielded results, display the first result and set an
        # index to 0, which will be used for paging through the results.
        if self.search_results:
            index = 0
            while True:
                print(
                    "Displaying result "
                    "{} of {}".format(index + 1, len(self.search_results))
                )
                try:
                    current_result = Log(**self.search_results[index])
                    current_result.display_log()
                except TypeError:
                    input(
                        "Oh no! It looks like the data in work_logs.txt is "
                        "not formatted correctly!\nPress any key to return to "
                        "the Search Menu."
                    )
                else:
                    # Display navigation options for the search result detail
                    # view.
                    nav = input(
                        "[N]ext, [P]revious, [E]dit, [D]elete, "
                        "[R]eturn to Search Menu: "
                    ).lower()

                    # Page to next result (if any)
                    if nav == 'n' and index != len(self.search_results) - 1:
                        index += 1
                
                    # Page to previous result (if any)
                    if nav == 'p' and index != 0:
                        index -= 1
            
                    # Enter edit log dialogue.
                    if nav == 'e':
                        current_result.edit_log()
                        break
            
                    # Enter delete log dialogue.
                    if nav == 'd':
                        if confirm_user_action():
                            current_result.delete_log()
                        break
            
                    # Break search result detail view loop if [R]eturn is
                    # selected.
                    if nav == 'r':
                        break
                
                    # Keep loop going if navigation input is invalid.
                    else:
                        clear_screen()
                        continue
    
        # If no search results, announce that and leave search result detail
        # view.
        else:
            nav = input(
                "---Sorry, no results matched your search.---"
                "\nPress any key to return to the Search Menu."
            )
            pass


