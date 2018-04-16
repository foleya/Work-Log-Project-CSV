import csv
import sys

from user_navigation_functions import clear_screen


def clear_all_logs():
    '''Clears/Deletes all work logs'''
    confirm = input("Enter 'CLEAR' to clear all logs.").lower()

    if confirm == 'clear':
        with open('work_log.txt', 'w+') as work_log:
            work_log.write('date,task_name,time_spent,note\n')
        input(
            "All work logs have been cleared. "
            "Hit 'Enter' to return to the Main Menu."
        )

    else:
        input(
            "Work logs have been preserved. "
            "Hit 'Enter' to return to the Main Menu."
        )


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
            work_log.write('date,task_name,time_spent,note\n')
        return True

    # If pre_existing work_log.txt uses wrong (or no) headers, exit the program
    # while prompting the user to fix the headers.
    else:
        with open("work_log.txt", "r") as work_log:
            if work_log.readline() != 'date,task_name,time_spent,note\n':
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



