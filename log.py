import csv

from csv_functions import fetch_logs
from user_navigation_functions import (clear_screen, confirm_user_action, menu)
from user_input_functions import (get_valid_date_format, get_valid_string,
                                  get_valid_time_spent)


class Log():
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_log_date(self):
        '''Updates a log's date_attribute'''
        print("Enter the date of this work.")
        self.date = get_valid_date_format()
    
    def get_log_task_name(self):
        '''Updates a log's task_name attribute'''
        self.task_name = get_valid_string('task name')
    
    def get_log_time_spent(self):
        '''Updates a log's time_spent attribute'''
        self.time_spent = get_valid_time_spent()

    def get_log_note(self):
        '''Updates a log's note attribute'''
        self.note = get_valid_string('note')
                
    def get_all_log_fields(self):
        '''Get all log attributes'''
        clear_screen()
        self.get_log_date()
        self.get_log_task_name()
        self.get_log_time_spent()
        self.get_log_note()

    def copy_log(self, copied_log):
        '''Copies the attributes of another log class instance'''
        self.__dict__ = copied_log.__dict__.copy()
    
    def display_log(self):
        '''Displays the attributes of a work log as a formatted string'''
        print(
            "Date: {d}\n"
            "Task Name: {t}\n"
            "Time Spent: {m} Minutes\n"
            "Note: {n}\n".format(
                d=self.date,
                t=self.task_name,
                m=self.time_spent,
                n=self.note)
        )
     
    def add_log(self):
        '''Appends comma separated attributes of a work log to work_log.txt'''
        with open('work_log.txt', 'a+', newline='') as work_log:
            logwriter = csv.writer(
                work_log,
                delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )
            logwriter.writerow(
                [self.date] + [self.task_name] +
                [self.time_spent] + [self.note]
            )
    
    def create_new_log(self):
        '''Get a new log from the user and write it to work_log.txt'''
        self.get_all_log_fields()
        self.add_log()
        clear_screen()
        print("New work log created:")
        self.display_log()
        input("\nHit 'Enter' to return to the Main Menu.")
    
    def delete_log(self):
        '''
        Deletes a log from work_log.txt
    
        This rewrites the work_log.txt file, excluding a specific log the user
        has chosen to delete. To do this, first, all the logs from fetch_logs()
        are given their line numbers in the csv (with enumerate). Then the log
        to be deleted is matched with its line number, allowing the file to be
        rewritten with the exclusion of the line number associated with the
        log to be deleted.
        '''
        # Create a list of logs matched with their "line numbers" by using
        # enumerate.
        logs_with_line_numbers = list(enumerate(fetch_logs(), 1))
    
        # For any log in that numbered list, if it has details that match the
        # log scheduled for deletion, add its "line number" to a list of line
        # numbers to be deleted.
        line_numbers_to_delete = []
        for num, log in logs_with_line_numbers:
            if {
                'date': self.date,
                'task_name': self.task_name,
                'time_spent': self.time_spent,
                'note': self.note
            } == log:
                line_numbers_to_delete.append(num)

        # Re-write the work_logs.txt file, excluding any lines with
        # line numbers that were scheduled for deletion. Line numbers are again
        # generated with enumerate (and the header line is set to be 0).
        with open("work_log.txt", "r+") as work_log:
            data = work_log.readlines()
            work_log.seek(0)
            for line_num, line in enumerate(data, 0):
                if line_num not in line_numbers_to_delete:
                    work_log.write(line)
            work_log.truncate()

    def edit_log(self):
        '''
        Prompts a user to edit chosen attributes of a log
    
        Using a dictionary of options to generate a menu, this asks whether the
        user would like to edit the date, title, duration, and/or note for a
        work log. The desired fields are retrieved, then a new log with the
        editted and original fields (if any) is appended to work_log.txt --
        while the original log is deleted from work_log.txt
        '''
        edit_options = {
            '1': 'Date',
            '2': 'Task Name',
            '3': 'Time Spent',
            '4': 'Note',
            '5': 'All Fields',
            '6': 'No Fields (Return to Search Menu)'
        }
        # Display the log the user desires to edit and present them with the
        # edit menu, getting their chosen action.
        
        clear_screen()
        print("Original Log:")
        self.display_log()
        print("\nWhat field(s) would you like to edit?")
        edit_field = menu(edit_options)

        # Return the user to the search menu if no edits are desired.
        if edit_field == 'No Fields (Return to Search Menu)':
            pass
        
        # User desires to edit fields in the log.
        else:
            # If edits are desired, create a copy of the original log for
            # editing. Keeping the original log instance to display to the user
            # when evaluating edits, and also to be used for deletion if the
            # edits are later confirmed.
            edited_log = Log()
            edited_log.copy_log(self)
            
            # Execute edits for chosen fields.
            if edit_field == 'Date':
                edited_log.get_log_date()

            if edit_field == 'Task Name':
                edited_log.get_log_task_name()

            if edit_field == 'Time Spent':
                edited_log.get_log_time_spent()

            if edit_field == 'Note':
                edited_log.get_log_note()

            if edit_field == 'All Fields':
                edited_log.get_all_log_fields()
                
            # Display the original and editted logs to the user.
            clear_screen()
            self.display_log()
            print("\n--- Will Be Replaced With---\n")
            edited_log.display_log()

            # Update work_log.txt if the user confirms their edits by adding
            # the jeditted log, and deleting the original log.
            if confirm_user_action():
                edited_log.add_log()
                self.delete_log()
