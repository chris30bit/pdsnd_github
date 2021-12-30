import datetime as dt
import time
import pandas as pd
import numpy as np
import os

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            'Please type in one these cities? Chicago, New York City or Washington: ').lower()
        if city in CITY_DATA:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month_dict = {'january': '01', 'february': '02', 'march': '03', 'april': '04', 'may': '05', 'june': '06',
                      'july': '07', 'august': '08', 'september': '09', 'october': '10', 'november': '11', 'december': '12', 'all': 'all'}
        month = input(
            'If you want to filter by month, type in any month,  otherwise type \"all\" : ').lower()
        print(month)
        if month in month_dict:
            month = month_dict[month]
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            'Please select the day you want to explore. ("all"or monday, tuesday, ... sunday)": ').lower()
        if (day == 'all') or (day == 'monday') or (day == 'tuesday') or (day == 'wednesday') or (day == 'thursday') or (day == 'friday') or (day == 'saturday') or (day == 'sunday'):
            break

    if (month == 'all'):
        print("\nYou like to explore the bike rentals of {} in 2017: ".format(city))
    else:
        print(
            "\nYou like to explore the bike rentals of {} in 2017-{}: ".format(city, month))
    if(day != 'all'):
        print('\nThe rentals are filtered to {}\'s only !'.format(day))

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
    # print(CITY_DATA[city])

    df = pd.read_csv(CITY_DATA[city], sep=',')  # .head(60)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Trip Duration'] = pd.to_numeric(df['Trip Duration'])
    df['week_day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['Connections'] = df['Start Station'] + ' - ' + df['End Station']
    if (month != 'all'):
        df = df[(df['Start Time'].dt.month == int(month))]
    if(day != 'all'):
        df = df[(df['Start Time'].dt.weekday ==
                 time.strptime(day, '%A').tm_wday)]
    # print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        none"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                  7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    # display the most common month
    mcm = df.groupby('month').count()
    max_rentals_month = mcm.max().max()
    month = int(mcm[(mcm == max_rentals_month).any(axis=1)].index[0])
    print("\tThe most common month was {}! \n\tThere were {} rentals during this month!".format(
        month_dict[month], max_rentals_month))

    # display the most common day of week
    weekday_dict = {0: 'monday', 1: 'Tuesday', 2: 'Wednesday',
                    3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    mc_wd = df.groupby('week_day').count()
    max_rentals_weekday = mc_wd.max().max()
    weekday = int(mc_wd[(mc_wd == max_rentals_weekday).any(axis=1)].index[0])
    print("\n\tThe most common weekday was {}! \n\tThere were {} rentals on this weekday!".format(
        weekday_dict[weekday], max_rentals_weekday))

    # display the most common start hour
    mc_h = df.groupby('hour').count()
    max_rentals_hour = mc_h.max().max()
    hour = int(mc_h[(mc_h == max_rentals_hour).any(axis=1)].index[0])
    print("\n\tThe most common hour was at {} o clock! \n\tThere were {} rentals during this hour!".format(
        hour, max_rentals_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        none"""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_stst = df.groupby('Start Station').count()
    max_stst = mc_stst.max().max()
    mc_stst = mc_stst[(mc_stst == max_stst).any(axis=1)].index[0]
    print("\tThe most common start station was " + mc_stst+".")

    # display most commonly used end station
    mc_etst = df.groupby('End Station').count()
    max_etst = mc_etst.max().max()
    mc_etst = mc_etst[(mc_etst == max_etst).any(axis=1)].index[0]
    print("\n\tThe most common end station was " + mc_etst+".")

    # display most frequent combination of start station and end station trip
    mc_conn = df.groupby('Connections').count()
    max_conn = mc_conn.max().max()
    # print(max_conn)
    mc_conn = mc_conn[(mc_conn == max_conn).any(axis=1)].index[0]
    print("\n\tThe most common connection was " + mc_conn+".")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        none"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print("\n\tThe cumulated travel time was: {} seconds".format(travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\n\tThe mean travel time was: {} seconds".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        none"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    customer_count = df[(df['User Type'] == 'Customer')]['User Type'].count()
    subsribed_customer_count = df[(
        df['User Type'] == 'Subscriber')]['User Type'].count()
    print("\n\tThere were {} subscribed customers and {} unsubscribed customers".format(
        subsribed_customer_count, customer_count))

    # Display counts of gender
    try:
        males = df[(df['Gender'] == 'Male')]['Gender'].count()
        females = df[(df['Gender'] == 'Female')]['Gender'].count()
        print("\n\tThere were {} female and {} male customers.".format(males, females))
    except:
        print("\n\tThere is no data about gender of customers available!")

    # Display earliest, most recent, and most common year of birth
    try:
        min_birth_year = df['Birth Year'].min()
        print("\n\tThe oldest customer was born in {}".format(min_birth_year))
    except:
        print("\n\tThere is no data about age of customers available!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays 5 lines of raw data, if wanted.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        none"""
    df = df.drop('week_day', 1)
    df = df.drop('hour', 1)
    df = df.drop('month', 1)
    df = df.drop('Connections', 1)
    view_data = input(
        "Would you like to view 5 rows of individual trip data? Enter yes or no! ").lower()
    start_loc = 0
    size = df['Start Time'].count()
    while (view_data == 'yes'):
        if(start_loc+5) <= size:
            print(df.iloc[start_loc:start_loc + 5])
        else:
            print(df.iloc[start_loc:size])
            break
        start_loc += 5
        view_data = input("Do you wish to continue? ").lower()


def main():
    """Main function to control end of program and sub function calls

    Args: none        
    Returns: none"""
    i = 0
    while i < 1:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # check if any data are available to analyse
        if (df.empty):
            print("There are no data available for this time frame!")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no!\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
