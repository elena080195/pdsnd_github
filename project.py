import datetime
import pandas as pd
import calendar


def get_city():
    '''Asks the user to choose a city and returns the filename for the chosen city's data.
    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n').title()
    if city == 'Chicago' or city == 'C':
        return 'chicago.csv'
    elif city == 'New York' or city == "N":
        return 'new_york_city.csv'
    elif city == 'Washington' or city == 'W':
        return 'washington.csv'
    else:
        print('\nPlease, type either the name of the city or its abbreviation.'
             'E.g. Chicago or C / New York or N / Washington or W')
        return get_city()


def get_time_period():
    '''Asks the user to choose a time period and returns the specified filter
    Args:
        none.
    Returns: The type of filter period the user's chosen (e.g. month, day, none);
             The specific filter period (e.g. January, February, Monday, Tuesday)
    '''
    time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "month" or "day" or "none".\n').lower()
    if time_period == 'month' or time_period == 'm':
        return ['month', get_month()]
    elif time_period == 'day' or time_period == 'd':
        return ['day', get_day()]
    elif time_period == 'none' or time_period == 'n':
        return ['none', 'no filter']
    else:
        print("\nI'm sorry, but something went wrong. I'm not sure which time period you've chosen'. Let's try again.")
        return get_time_period()

def get_month():
    '''Asks the user to choose a month and returns the specified month.
    Args:
        none.
    Returns:
        (str) String representation of month number (e.g. January - 01, Febraury - 02)
    '''

    month = input('\nWhich month you\'d like to filter the data? January, February, March, April, May, or June?\n').title()
    if month == 'January' or  month == 'J':
        return '01'
    elif month == 'February' or  month == 'F':
        return '02'
    elif month == 'March' or  month == 'Mar':
        return '03'
    elif month == 'April' or  month == 'A':
        return '04'
    elif month == 'May':
        return '05'
    elif month == 'June' or  month == 'Ju':
        return '06'
    else:
        print("\nI'm sorry, but something went wrong. I'm not sure which month you've chosen'. Let's try again.")
        return get_month()

def get_day():
    '''Asks the user to choose a day of the week they want to filter the data for and returns the specified day.
    Args:
        none.
    Returns:
        (int) Represents the day of the week (e.g. Monday - 0, Tuesday - 1)
    '''
    day_of_week = input('\nWhich day of the week you\'d like to filter the data?'
                       ' Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
    if day_of_week == 'Monday' or day_of_week == 'M':
        return 0
    elif day_of_week == 'Tuesday' or day_of_week == 'Tu':
        return 1
    elif day_of_week == 'Wednesday' or day_of_week == 'W':
        return 2
    elif day_of_week == 'Thursday' or day_of_week == 'Th':
        return 3
    elif day_of_week == 'Friday' or day_of_week == 'F':
        return 4
    elif day_of_week == 'Saturday' or day_of_week == 'Sat':
        return 5
    elif day_of_week == 'Sunday' or day_of_week == 'Sun':
        return 6
    else:
        print("\nI'm sorry, but something went wrong. I'm not sure which day of the week you've chosen. Let's try again.")
        return get_day()

def get_popular_month(df):
    '''Returns a month with the highest number of trips.
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String displays a month with the highest number of trips
    '''
    numb_trips_by_month = df.groupby('Month')['Start Time'].count()
    return "The most popular month for start time is " + calendar.month_name[int(numb_trips_by_month.sort_values(ascending=False).index[0])]

def get_popular_day(df):
    '''Returns a day with the highest number of trips.
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String displays a day with the highest number of trips
    '''
    numb_trips_by_day = df.groupby('Day of Week')['Start Time'].count()
    return "The most popular day of the week for start time is " + calendar.day_name[int(numb_trips_by_day.sort_values(ascending=False).index[0])]

def get_popular_hour(df):
    '''Returns the hour of the day with the highest number of trips.
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String displays which hour of the day had the highest number of trips.
    '''
    numb_trips_by_hour = df.groupby('Hour of Day')['Start Time'].count()
    most_pop_hour_int = numb_trips_by_hour.sort_values(ascending=False).index[0]
    d = datetime.datetime.strptime(most_pop_hour_int, "%H")
    return "The most popular hour of the day for start time is " + d.strftime("%I %p")

def trip_duration(df):
    '''Given a dataframe of bikeshare data, this function returns the total trip duration and average trip duration
    Args:
        df: dataframe of bikeshare data
    Returns:
            First value: The total trip duration in years, days, hours, minutes, and seconds
            Second value: The average trip duration in hours, minutes, and seconds
    '''
    total_trip_duration = df['Trip Duration'].sum()
    avg_trip_duration = df['Trip Duration'].mean()
    m, s = divmod(total_trip_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    total_trip_duration = "\nTotal trip duration: %d year(s) %02d day(s) %02d hour(s) %02d min %02d sec" % (y, d, h, m, s)
    m, s = divmod(avg_trip_duration, 60)
    h, m = divmod(m, 60)
    avg_trip_duration = "Average trip duration: %d hour(s) %02d min %02d sec" % (h, m, s)
    return [total_trip_duration, avg_trip_duration]

def popular_trip(df):
    '''Given a dataframe of bikeshare data, this function returns the most popular trip (i.e. combination of start station and end station)
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String that says the most popular combination of start and end
        stations as well as how many trips that accounted for and what
        percentage of trips that accounted for
    '''
    trip_counts = df.groupby(['Start Station', 'End Station'])['Start Time'].count()
    sorted_trip_stations = trip_counts.sort_values(ascending=False)
    total_trips = df['Start Station'].count()
    return "The most popular trip: " + "\n  Start station: " + str(sorted_trip_stations.index[0][0]) + "\n  End station: " + str(sorted_trip_stations.index[0][1]) + "\n  (" + str(sorted_trip_stations[0]) +  " trips, " + '{0:.2f}%'.format(((sorted_trip_stations[0]/total_trips) * 100)) + " of trips)"

def popular_stations(df):
    '''Given a dataframe of bikeshare data, this function returns the most popular start and end stations
    Args:
        df: dataframe of bikeshare data
    Returns:
            First value: The name of the most popular start station
                and how many trips started from there and what percentage of trips
                that accounted for
            Second value: The name of the most popular end station and how many trips started
            from there and what percentage of trips
                that accounted for
    '''
    start_station_counts = df.groupby('Start Station')['Start Station'].count()
    end_station_counts = df.groupby('End Station')['End Station'].count()
    sorted_start_stations = start_station_counts.sort_values(ascending=False)
    sorted_end_stations = end_station_counts.sort_values(ascending=False)
    total_trips = df['Start Station'].count()
    most_popular_start_station = "\nMost popular start station: " + sorted_start_stations.index[0] + " (" + str(sorted_start_stations[0]) + " trips, " + '{0:.2f}%'.format(((sorted_start_stations[0]/total_trips) * 100)) + " of trips)"
    most_popular_end_station = "Most popular end station: " + sorted_end_stations.index[0] + " (" + str(sorted_end_stations[0]) + " trips, " + '{0:.2f}%'.format(((sorted_end_stations[0]/total_trips) * 100)) + " of trips)"
    return [most_popular_start_station, most_popular_end_station]

def users(df):
    '''Returns the number of trips by user type
    Args:
        df: dataframe of bikeshare data
    Returns:
        (pandas series) where the index of each row is the user type and the value
            is how many trips that user type made
    '''
    user_type_counts = df.groupby('User Type')['User Type'].count()
    return user_type_counts

def gender(df):
    '''Returns the number of trips by gender
    Args:
        df: dataframe of bikeshare data
    Returns:
        (pandas series) where the index of each row is the gender and the value
            is how many trips that gender made
    '''
    gender_counts = df.groupby('Gender')['Gender'].count()
    return gender_counts


def birth_years(df):
    '''Given a dataframe of bikeshare data, this function returns the oldest
        birth year, the most recent birth year, and the most common birth year
    Args:
        df: dataframe of bikeshare data
    Returns:
            First value: The earliest birth year of anyone who made a trip
            Second value: The most recent birth year of anyone who made a trip
            Third value: The most common birth year of people who made a trip
    '''
    earliest_birth_year = "The earliest birth year: " + str(int(df['Birth Year'].min()))
    most_recent_birth_year = "The most recent birth year: " + str(int(df['Birth Year'].max()))
    birth_year_counts = df.groupby('Birth Year')['Birth Year'].count()
    sorted_birth_years = birth_year_counts.sort_values(ascending=False)
    total_trips = df['Birth Year'].count()
    most_common_birth_year = "The most common birth year: " + str(int(sorted_birth_years.index[0])) + " (" + str(sorted_birth_years.iloc[0]) + " trips, " + '{0:.2f}%'.format(((sorted_birth_years.iloc[0]/total_trips) * 100)) + " of trips)"
    return [earliest_birth_year, most_recent_birth_year, most_common_birth_year]

def display_data(df, current_line):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more.
    Continues asking until they say stop.
    Args:
        df: dataframe of bikeshare data
    Returns:
        If the user says yes then this function returns the next five lines
            of the dataframe and then asks the question again by calling this
            function again (recursive)
        If the user says no then this function returns, but without any value
    '''
    display = input('\nWould you like to view individual trip data?'
                    ' Type \'+\' for YES or \'-\' for NO.\n')
    display = display.lower()
    if display == 'yes' or display == 'y' or display == '+'  :
        print(df.iloc[current_line:current_line+5])
        current_line += 5
        return display_data(df, current_line)
    if display == 'no' or display == 'n' or display == '-' :
        return
    else:
        print("\nI'm sorry, but something went wrong. Let's try again.")
        return display_data(df, current_line)


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()
    city_df = pd.read_csv(city)

    def get_day_of_week(str_date):
        '''Takes a date in the format yyyy-mm-dd and returns an integer
            represention of the day of the week, e.g. for Monday it returns 0
        Args:
            str_date: date in the format yyyy-mm-dd
        Returns:
            (int) Integer represention of the day of the week,
                e.g. for Monday it returns 0
        '''
    #parse string in format yyyy-mm-dd and create date object based on those values.
        date_obj = datetime.date(int(str_date[0:4]), int(str_date[5:7]), int(str_date[8:10]))
        return date_obj.weekday() #return the day of the week that that date was
    #store day of week, month, and hour of day values for each
    #row in their own columns. Makes it easier to groupby those values later
    city_df['Day of Week'] = city_df['Start Time'].apply(get_day_of_week)
    city_df['Month'] = city_df['Start Time'].str[5:7]
    city_df['Hour of Day'] = city_df['Start Time'].str[11:13]

    # Filter by time period that the user chose (month, day, none)
    time_period = get_time_period()
    filter_period = time_period[0]
    filter_period_value = time_period[1]
    filter_period_label = 'No filter'

    if filter_period == 'none':
        filtered_df = city_df
    elif filter_period == 'month':
        filtered_df = city_df.loc[city_df['Month'] == filter_period_value]
        filter_period_label = calendar.month_name[int(filter_period_value)]
    elif filter_period == 'day':
        filtered_df = city_df.loc[city_df['Day of Week'] == filter_period_value]
        filter_period_label = calendar.day_name[int(filter_period_value)]

    #Prints which city this data is for and any filters that were applied
    print('\n')
    print(city[:-4].upper().replace("_", " ") + ' -- ' + filter_period_label.upper())
    print('-------------------------------------')

    #To give some context, print the total number of trips for this city and filter
    print('Total trips: ' + "{:,}".format(filtered_df['Start Time'].count()))

    # The most popular month for start time
    if filter_period == 'none' or filter_period == 'day':
        print(get_popular_month(filtered_df))

    # The most popular day of week for start time
    if filter_period == 'none' or filter_period == 'month':
        print(get_popular_day(filtered_df))

    # The most popular hour of day for start time
    print(get_popular_hour(filtered_df))

    # The total trip duration and average trip duration
    trip_duration_stats = trip_duration(filtered_df)
    print(trip_duration_stats[0])
    print(trip_duration_stats[1])

    # The most popular start and end stations
    most_popular_stations = popular_stations(filtered_df)
    print(most_popular_stations[0])
    print(most_popular_stations[1])

    # The most popular trip
    print(popular_trip(filtered_df))

    # Counts of user types
    print('')
    print(users(filtered_df))

    # Only Chicago and New York have gender and birth years columns
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        # The counts of genders
        print('')
        print(gender(filtered_df))
        # The oldest user, youngest user, and the most popular birth years
        birth_years_data = birth_years(filtered_df)
        print('')
        print(birth_years_data[0])
        print(birth_years_data[1])
        print(birth_years_data[2])

    # Displays five lines of data at a time if user chooses that they would like to
    display_data(filtered_df, 0)

    def restart_question():
        '''Asks the user if they want to restart the program. If the user chooses yes, restarts it.
        If no - ends the program.
        '''
        restart = input('\nWould you like to restart? Type \'+\' for YES or \'-\' for NO. If you choose  \'-\' the session will end\n')
        if restart.lower() == 'yes' or restart.lower() == 'y' or restart == '+':
            statistics()
        elif restart.lower() == 'no' or restart.lower() == 'n' or restart == '-' :
            return
        else:
            print("\nI'm sorry, but something went wrong. Let's try again.")
            return restart_question()

    restart_question()


if __name__ == "__main__":
    statistics()
