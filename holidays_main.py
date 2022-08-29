from dataclasses import dataclass, field
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from datetime import date
#from config import api_key (I would include if I included the weather API)

changes = False
is_running = True

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    name: str
    date: datetime
        
    def __str__ (self):
        return (f'{self.name} {self.date}')
    #     # String output
    #     # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class Holiday_List:
    def __init__(self):
        self.inner_holidays = []
    
    def start_up(self):
        print(f'Holiday Management \n================ \nThere are {self.num_holidays()} holidays stored in the system')

    def main_menu(self):
        #yes I know it's long but it works!
        menu_options = """
1: Add a Holiday
2: Remove a Holiday
3: Save Holiday List
4: View Holidays
5: Exit"""
        while True:
            print(f'{menu_options}')   
            while True:
                try:
                    user_input = int(input('\nSelect a menu option [1-5]: '))
                    if user_input >= 1 and user_input <6:
                        break
                    else:
                        print('Please enter a number in range')
                except ValueError:
                    print('That is not a number, try again')
            
            if user_input == 1:
                            
                while True:
                    print('Add a Holiday \n=============')
                    holiday_name = str(input('Holiday: '))
                    break
                while True:
                    holiday_date = str(input('Date YYYY-MM-DD: '))
                    try:
                        date.fromisoformat(holiday_date)
                        holiday_obj = Holiday(holiday_name, holiday_date)
                        self.add_holiday(holiday_obj)
                        break
                    except:
                        print('Date is not valid. Try Again')
                        

            elif user_input == 2:
                while True:
                    print('Remove a Holiday \n================')
                    holiday_name = str(input('Holiday: '))
                    holiday_date = str(input('Date: YYYY-MM-DD: '))
                    self.remove_holiday(holiday_name, holiday_date)
                    break

            elif user_input == 3:
                global changes
                while True:
                    print('Saving Holiday List \n====================')
                    save_changes = str(input('Are you sure you want to save your changes? [y/n]: '))
                    if save_changes == 'y':
                        self.save_to_json('holidays_updated')
                        print('Success: \nYour changes have been saved')
                        changes = False
                        break
                    else:
                        print('Canceled: \n Holiday list file save canceled')
                        break
            elif user_input == 4:
                while True:
                    print('View Holidays \n=============')
                    holiday_year = str(input('Which year?: '))
                    holiday_week = str(input('Which week? #[1-52, leave blank for current week]: '))
                    if holiday_week == '':
                        self.view_current_week()
                        break
                    else:
                        holidays = self.filter_holidays_by_week(holiday_year, holiday_week)
                        print(f"These are the holidays for {holiday_year} week #{holiday_week}\n")
                        self.display_holidays_in_week(holidays)
                        break
            elif user_input == 5:
                global is_running
                print('Exit \n====')
                if changes == False:
                    exit = str(input('Are you sure you want to exit? [y/n]: '))
                    if exit == 'y':
                        print('Goodbye!')
                        is_running = False
                        break
                else:
                    exit_no_save = str(input('Are you sure you want to exit?\nYour changes will be lost\n[y/n]: '))
                    if exit_no_save == 'y':
                        print('Goodbye!')
                        is_running = False
                        break
            else:
                print('Please select a number [1-5]')
    
    
    def add_holiday(self, holiday_obj):
        global changes
        exsisting_holiday = holiday_obj in self.inner_holidays
        while changes == False:
            if exsisting_holiday == False:
                self.inner_holidays.append(holiday_obj)
                print(f'Success: \n{holiday_obj} has been added to the holiday list')
                changes = True
            else:
                print('Holiday is already included')

        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def find_holiday(self, holidayName, date):
        for i in self.inner_holidays:
            inner_holidays_dict = self.inner_holidays[i].__dict__
            if holidayName == inner_holidays_dict['name'] and date == inner_holidays_dict['date']:
                return f"{inner_holidays_dict['name']} {inner_holidays_dict['date']}"

        # Find Holiday in innerHolidays
        # Return Holiday

    def remove_holiday(self, holidayName, date):
        global changes
        for i in self.inner_holidays:
            if i.name == holidayName and i.date == date:
                self.inner_holidays.remove(i)
                print (f'Success: \n{i} has been removed from the holiday list')
                changes = True
                break
            else:
                print(f'Error: \n {holidayName} not found')
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self, file_location):
        holidays_file = open(file_location).read()
        holidays_file_json = json.loads(holidays_file)
        for i in holidays_file_json['holidays']:
            holiday_object = Holiday(i['name'],i['date'])
            self.inner_holidays.append(holiday_object)
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self, file_loc):
        holiday_list = [i.__dict__ for i in self.inner_holidays]
        holiday_dict = {
            'holidays' : holiday_list
        }
        with open(file_loc, 'w') as save_file:
            json.dump(holiday_dict, save_file)
        # Write out json file to selected file.
        # From a holiday list, create a dictionary for the holidays to be saved into the json file intended.

    def scrape_holidays(self):
        years = ['2020', '2021', '2022', '2023', '2024']

        for i in years:
            url = f'https://www.timeanddate.com/holidays/us/{i}'
            print(f'Scraping url: {url}') 
            
            resp = requests.get(url)
            resp_text = resp.text
            soup = BeautifulSoup(resp_text, 'html.parser')
            all_holidays = soup.find('tbody')
            names = all_holidays.find_all('a')
            dates = all_holidays.find_all('th')
    
            for x in range(len(dates)):
                date_month = dates[x].string
                date_mdy = date_month + ', '+(i)
                holiday_date = datetime.strptime(date_mdy,'%b %d, %Y').strftime('%Y-%m-%d')
                holiday_name = names[x].string

                holiday_object = Holiday(holiday_name, holiday_date)
                exsisting_holiday = holiday_object in self.inner_holidays
                if exsisting_holiday == False:
                    self.inner_holidays.append(holiday_object)
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def num_holidays(self):
        return len(self.inner_holidays)
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        holidays_list_dict = [i.__dict__ for i in self.inner_holidays]
        holidays_list = list(filter(lambda i: str(date.fromisoformat(i['date']).isocalendar().week) == str(week_number) and str(date.fromisoformat(i['date']).isocalendar().year) == str(year), holidays_list_dict))
        return holidays_list
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def display_holidays_in_week(self, list_holidays):
        
        holiday_objects_filter = []
        for i in range(len(list_holidays)):            
            holiday_objects_filter.append(Holiday(list_holidays[i]['name'], list_holidays[i]['date']))
        for x in holiday_objects_filter:
            print(x)
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    def view_current_week(self):
        now = datetime.now()
        current_week = now.date().isocalendar().week
        current_year = now.date().isocalendar().year
        current_holidays = self.filter_holidays_by_week(current_year, current_week)
        self.display_holidays_in_week(current_holidays)
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results



def main():
    
    init_holiday_list = Holiday_List()
    init_holiday_list.read_json('holidays.json')
    init_holiday_list.scrape_holidays()
    init_holiday_list.start_up()
    while is_running == True:
        init_holiday_list.main_menu()
        
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
main()
# if __name__ == "__main__":
#     main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.

