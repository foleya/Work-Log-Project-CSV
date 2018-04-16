import datetime
import re


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


def get_valid_string(field):
    '''
    Prompts the user to enter a task_name or note with valid characters
    
    This prompts the user to enter text, ensuring that the text entered is not
    surrounded by doublequotes and (for the most) part has normal characters --
    both of which would be problematic for the csv.DictReader fetch_logs() uses
    to read the work_log.txt file.
    
    Argument: String (Field 'type' to be used for formatting the prompt)
    Returns: String (Field text compatible with csv.DictReader)
    '''
    while True:
        text = input('Enter a {} for this log: '.format(field))
        if text[0] == '"' and text[-1] == '"':
            print(
                "\n---Sorry! The note field cannot be surrounded by "
                "doublequotes. Try again.---\n"
            )
        elif not re.match(r'^[-\w\d\s.,!\(\);:\'"?]+$', text):
            print(
                "---\nSorry! Invalid characters detected. Please stick to "
                "using alphanumerics and normal punctuation. Try again!"
                "---\n"
            )
        elif text == '':
            text = 'None'
            break
        else:
            break
    return text


def get_valid_time_spent():
    '''Prompts user to enter time_spent in rounded minutes'''
    while True:
        time_spent = input('Enter time spent in minutes (rounded): ')
        try:
            int(time_spent)
        except ValueError:
            print(
                "\n--- Sorry, '{}' is not a whole number. "
                "Please enter a whole number. ---\n".format(time_spent)
            )
        else:
            break
    return time_spent
