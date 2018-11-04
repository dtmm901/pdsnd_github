import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('\nEnter one of the following city name: Chicago, New\
            York City or Washington:\n').lower()
            if city.lower() not in ('chicago', 'new york city', 'washington'):
                raise NameError
            break
        except:
            print('\nOops! That was not a correct city name. Try again..')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('\nEnter month name in full, e.g. May or \'all\' for \
            no month filter:\n').lower()
            if month.lower() not in ('january', 'february', 'march', 'april',
            'may', 'june', 'all'):
                raise NameError
            break
        except:
            print('\nOops! That was not a correct month name. Try again..')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('\nEnter day name in full, e.g. Monday or \'all\' for \
            no day filter:\n').lower()
            if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday', 'all'):
                raise NameError
            break
        except:
            print('\nOops! That was not a correct day name. Try again..')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df.loc[df['month'] == month]

    if day != 'all':
        df = df.loc[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (mc_month)
    # df['month'].value_counts() is a pandas series and index is int64
    mc_month = df['month'].value_counts().idxmax()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    mc_month = months[mc_month-1].title()
    print('The most common month is : {}\n'.format(mc_month))

    # display the most common day of week (mc_dow)
    mc_dow = df['day'].value_counts().idxmax()
    print('The most common day of week is : {}\n'.format(mc_dow))

    # display the most common start hour (mc_sh)
    df['hour'] = df['Start Time'].dt.hour
    mc_sh = df['hour'].value_counts().idxmax()
    print('The most common start hour is : {}\n'.format(mc_sh))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station (mc_used_start)
    mc_used_start = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is : {}\n'.format(mc_used_start))

    # display most commonly used end station (mc_used_end)
    mc_used_end = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station is : {}\n'.format(mc_used_end))

    # display most frequent combination of start station and end station trip (mf_combin)
    # a new column 'combin' shows the combination of start and end station of each trip
    df['combin'] = df['Start Station'].map(str) + ' & ' + df['End Station'].map(str)
    mf_combin = df['combin'].value_counts().idxmax()
    print('The most frequent combination of start station and end station trip is : {}\n'.format(mf_combin))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The total travel time is: {} seconds\n'.format(total_travel))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('The mean travel time is: {} seconds\n'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types, first check for null
    if (df['User Type'].isnull().any() == True):
        print('\nThere is null in the user type data\n')
    else:
        user_types = df['User Type'].value_counts()
        print('Counts of user types:\n', user_types)


    # Display counts of gender, earliest, most recent, and most common year of birth
    # First fill null with 'No record'
    try:
        df['Gender'].fillna('No record')
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:\n', gender_counts)
        earliest = df['Birth Year'].max().astype('int64')
        most_recent = df['Birth Year'].min().astype('int64')
        most_common = df['Birth Year'].idxmax().astype('int64')
        print('Earliest year of birth: {}\nMost recent year of birth: {}\n\
        Most common year of birth: {}\n'.format(earliest,most_recent,most_common))
    except:
        print('\nThere is no gender and birth year records for Washington\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """Displays DataFrame to users."""
    n = 5
    answer = input('\nDo you want to see the DataFrame? Type \'Yes\' to see\n').lower()
    if answer == 'yes':
        print(df.head(n))
        while True:
            answer = input('\nType \'Yes\' to see 5 more rows\n').lower()
            if answer == 'yes':
                n = n + 5
                print(df.head(n))
            else:
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
