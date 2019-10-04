import time
import sys
import calendar
import pandas as pd



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
monthslist = [calendar.month_name[i+1] for i in range (12)]
dowlist = list(calendar.day_name)

def timecnvrt(hour):
    """ This function converts hours from 24-hour format to 12-hour format.
    """
    if hour <12:
        ntm = '{} AM'.format(hour)
    elif hour >12:
        ntm = "{} PM".format(hour-12)
    elif hour == 12:
        ntm = "12 PM"
    return ntm

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city=input('Please choose a city name (Chicago, New York City or Washington) to analyze or type "exit" to exit the program: ').lower()
        if city.lower() in CITY_DATA:
            city=CITY_DATA[city]
            break
        elif city.lower() == 'exit':
            sys.exit('The program is now exiting.....')
    #added extra lines of code to detect the available months within the database and to prevent having an error when a month that is not available is entered.
    df = pd.read_csv(city)
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['Month']=pd.DatetimeIndex(df['Start Time']).month_name()
    print("The database has data for the following months only: \n{}." .format(df['Month'].unique()))
    
    while True:
        month=input("Please choose a month name from the list above, type all for no monthly filter or type 'exit' to exit the program: ").title()
        if month in monthslist and month in list(df['Month'].unique()):
            month=monthslist.index(month)+1
            break
        elif month.lower() == 'exit':
            sys.exit('The program is now exiting.....')
        elif month.lower() == 'all':
            month = 'all'
            break
        else:
            print("The month name you have entered is invalid, please try again.")

        
    while True:
        day=input('Please enter a day name (example: Monday, Tuesday, etc..) or type all for no monthly filter or type "exit" to exit the program: ').title()
        if day in dowlist:
            break
        elif day.lower() == 'exit':
            sys.exit('The program is now exiting.....')
        elif day.lower() == 'all':
            day = 'all'
            break
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(city)
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['Month']=pd.DatetimeIndex(df['Start Time']).month
    df['Day']=pd.DatetimeIndex(df['Start Time']).weekday_name
    
    if month != 'all':
        df = df[df['Month'] == month]
    
    if day != 'all':
        df = df[df['Day'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'all':
        print('The most common month is: ', calendar.month_name[(df['Month'].mode()[0])])
        
    if day == 'all':
        print('The most common day of week is: ', df['Day'].mode()[0])

    print('The most common start hour is: ', timecnvrt(df['Start Time'].dt.hour.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('The most commonly used start station is: ', 
          df['Start Station'].value_counts().index[0])  
    

    print('The most commonly used End station is: ', 
          df['End Station'].value_counts().index[0])  

    df['Trip Combination'] = 'From ' + df['Start Station'] +\
    ' to ' + df['End Station']
    print('The most frequent combination of start station and end station trip is: ',
          df['Trip Combination'].value_counts().index[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total travel time is: ', round(df['Trip Duration'].sum()/60, 2), ' minutes')
    
    print('Average trip duration is: ', round(df['Trip Duration'].mean()/60, 2), ' minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of user types:\n',df['User Type'].value_counts().to_string(), '\n')
    if city != 'washington.csv':
        print('Counts of user types: \n', df['Gender'].value_counts().to_string(), '\n')
        print('Earliest year of birth for users: ', int(df['Birth Year'].min()))
        print('Most Recent year of birth for users: ', int(df['Birth Year'].max()))
        print('Most common year of birth for users: ', int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    """this function takes the selected and filtered dataframe and presents 5 rows by 5 rows until the user asks it to stop
    """
    while True:
        userinput = input("Do you want to view the raw data? type 'yes' to view 5 lines of raw data or 'no' to exit: \n").lower()
        i=int()
        if userinput == 'yes':
            while i<df.shape[0]:
                print(df.iloc[i:i+5])
                i+=5
                suserinput = input("To view the next 5 rows of data press enter, to stop type 'stop'\n")
                if suserinput == '':
                    continue
                elif suserinput == 'stop':
                    x = print('you have viewed {} pages ({} rows) of data \n'.format(i, i*5),'-'*40)
                    return x
                    break

        elif userinput == 'no':
            return '-'*40
            break
        

def main():
    """ The main function creates a dataframe that is filtered by the user's input data, then uses this dataframe to provide statistics based on user requests."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
