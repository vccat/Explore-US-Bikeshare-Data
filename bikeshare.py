import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    input_tip = 'Data of three major cities are available: Chicago, New York City and Washington. \nPlease input the full name of the city you\'d like to explore or their initial(s), Thanks!\n'
    input_again = 'Sorry your input is not valid, please try again. \nOnly Chicago, New York City, Washington or their initial(s) are accepted.\n'
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_inputs = ['chicago', 'new york city', 'washington', 'c', 'nyc', 'w']
    temp_city = input(input_tip).lower()
    while temp_city not in valid_inputs:
        temp_city = input(input_again).lower()

    city = ('chicago' if temp_city in ['chicago', 'c'] else
            'new york city' if temp_city in ['new york city', 'nyc'] else
            'washington')

    # get user input for month (january, february, ... , june)
    input_month = 'Would you like to filter the data by month?\n January, February, March, April, May, June or No for no filter\n'
    valid_month_input = ['no', 'january',
                         'february', 'march', 'april', 'may', 'june']
    input_again_month = 'Sorry, your input is not valid, please try again. \nThe full name of the month for only the first 6 months or \'No\'\n'
    month = input(input_month).lower()
    while month not in valid_month_input:
        month = input(input_again_month).lower()
    if month == 'no':
        month = 'all'

    # get user input for day of week ( monday, tuesday, ... sunday)
    input_day = 'Would you also like to filter the data by day of week?\n Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or No for no filter.\n'
    input_again_day = 'Sorry, your input is not valid, please try again.'
    valid_day_input = ['no', 'monday', 'tuesday',
                       'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    day = input(input_day).lower()
    while day not in valid_day_input:
        day = input(input_again_day).lower()
    if day == 'no':
        day = 'all'

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
    # CITY_DATA = {'chicago': 'chicago.csv',
    #             'new york city': 'new_york_city.csv',
    #             'washington': 'washington.csv'}

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':

        # filter by month to create the new dataframe
        df = df[df.month == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].nunique() > 1:
        print('The most popular month of travel is:', df.month.mode().values)

    # display the most common day of week
    if df['day_of_week'].nunique() > 1:
        print('The most popular day of travel during the week is:',
              df.day_of_week.mode().values)

    # display the most common start hour
    print('The most common start hour of travel is',
          df['Start Time'].dt.hour.mode().values)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most popular Start Station(s): ',
          df['Start Station'].mode().values)

    # display most commonly used end station
    print('The most popular End Station(s): ', df['End Station'].mode().values)

    # display most frequent combination of start station and end station trip
    trip_size = df.groupby(['Start Station', 'End Station']).size()
    print('The most popular trip:')
    print(trip_size[trip_size == trip_size.max()])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    m, s = divmod(total_travel, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('The total travel time of your filtered data in {} is: '.format(city))
    print('{} days {} hours {} minutes and {} seconds'.format(
        int(d), int(h), int(m), s))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    m, s = divmod(mean_travel, 60)
    h, m = divmod(m, 60)
    print('And the average travel time is:\n {} hours, {} minutes and {} seconds.'.format(
        int(h), int(m), s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print('The breakdown of user type:')
    print(df.groupby('User Type').size())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\n')
        print('The breakdown of user gender:')
        print(df.groupby('Gender').size())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['Birth Year'] = df['Birth Year'].astype('Int64')
        print('\n')
        print('The earliest and most recent birth year of the users are {} and {}.'.format(
              df['Birth Year'].min(), df['Birth Year'].max()))
        print('The most common birth year(s) of users: ',
              df.groupby('Birth Year').size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def data_display(df):
    """Displays raw data that has been filtered by city, month and weekday as users wish. And each time 10 rows are displayed."""

    # get input of whether the user want to see some raw data
    show_data = input(
        'Now would you like to see the raw data, 10 rows each time? y - yes, n- no\n')
    start = 0
    end = len(df.index) - 1
    while show_data == 'y' and start < end:
        # print out the last few rows
        if start+10 >= end:
            print('Displaying the last few rows of data...')
            print(df.iloc[start:end+1, :])
            break
        # print out data 10 rows everytime when it's not the end.
        else:
            print('Displaying data from row {} to row {}...'.format(start, start+9))
            print(df.iloc[start:start+10, :])

        start += 10
        # get input of whether the user wannt to continue seeing the data.
        show_data = input(
            'Would you like to continue to see the next 10 rows? y-yes, n-no\n')


def main():
    while True:
        city, month, day = get_filters()
        print('OK! You have choosen {} in month {} and on the weekday {}'.format(
            city, month, day))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, city)
        user_stats(df)

        data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
