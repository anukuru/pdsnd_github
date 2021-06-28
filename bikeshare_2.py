
import time
import pandas as pd
import numpy as np
import calendar 
import datetime as date1

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
display_response =['yes','no']
                 

        

    
### FUNCTION DEFINITION TO GET USER FILTERS ###
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to #handle invalid inputs
    city_list=["chicago","new york", "washington"]
    month_list =["january", "february", "march", "april", "may", "june"]
    day_list = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
   
  
    while True:
      try:
        city = input("Pick a city for which you want to examine data . Your options are chicago or  new york or washigton: ")
        city=city.lower()
        #print("TEST", city)
        if city == "new york" or city == "chicago" or city == "washington":                
          print("City entered successfully...")
          break;
        else:
          print("City should be new york , chicago or washington")
      except:
        continue
            
               
    # get user input for month (all, january, february, ... , june)
    month_yes_no=input ("Would you like to filter by month? Type yes or no \n")

    if month_yes_no =='yes':
        while True:
             try:
               month = input("Pick a month for which you want to examine data . Your options are january, february, march,april, may, june: ")
               month=month.lower()
             #  print("TEST month", month)
               if month in month_list:                
                 print("Month entered successfully...")
                 break;
               else:
                 print("Please try again. Month options are nojanuary, february, march,april, may, june")
             except:
               continue
            
    
    
    else:
        month='all'
        print('Filter value for month: ', month)
     

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    dow_yes_no=input ("Would you like to filter by day of week? Type yes or no \n")

   
    if dow_yes_no =='yes':
        while True:
             try:
               dow = input("Pick a month for which you want to examine data . Your options are sunday, monday, tuesday, wednesdy, thursday, friday, saturday: ")
               dow=dow.lower()
             #  print("TEST dow", dow)
               if dow in day_list:                
                 print("Day of week entered successfully...")
                 break;
               else:
                 print("Please try again. Your options are sunday, monday, tuesday, wednesdy, thursday, friday, saturday: ")
             except:
               continue
    else:
        dow='all'
        
#load_data('chicago', 'february', 'Sunday')
#load_data(city, month,dow)
    return (city, month, dow)
            
##########################FUNCTION DEFITION TO LOAD DATA BASED ON FILTERS ###

  #  load_data(city, month, dow)
 
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
    print("All stats will be provided based on your filters : city = {}, month ={}, weekday = {}".format (city, month, day))
    df1 = pd.read_csv(CITY_DATA[city])
    
    # Extracting data to create new dataframe
    df1['Start Time'] = pd.to_datetime(df1['Start Time'])
    df1['month'] = df1['Start Time'].dt.month
    df1['day_of_week'] = df1['Start Time'].dt.weekday_name
   
    # Filtering
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df1 = df1[df1['month'] == month]
   
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df1 = df1[df1['day_of_week'] == day.title()]
         #  display (df1)
    trip_stats(df1, month, day)
    user_stats(df1)
    user_stats_gender_DOB (df1,city)
   # read_raw_data(df1)
    
    
    return (df1)
   



def trip_stats (df1, month, day):
    """
    calculates trip statistics
    1a. if city, month and day filters are entered by users: only popular hour is calculated
    1b. if city, month filters are entered and day filter is not entered by user : most popular day of the week is calculated in addition to hour
    1c. if only city filter is entered by the users: then popular hour, popular day of week and popular month is calculated
    
    2. Most common start station is calculated
    3. Most common end station is calculated
    4  Most common start and end station is calculated
    
    5. Duartion of trip: total duration and average duration is calcaulted
    
    Arguments:
    df1 = dataframe on which analysis is to be performed
    month= the month based on user input
    day = the day based on user inpyt
    
    Returns:
    none
    """
    
      
    ####### 1. POPULAR TIMES OF TRAVEL ###########################    
    ##common hour
    df1['hour'] = df1['Start Time'].dt.hour
    popular_hour = df1['hour'].mode()[0]
    print('POPULAR TIMES OF TRAVEL')
    print('Most Popular Start Hour:', popular_hour, '\n')
    
    if month=='all':
        print("Since we are not filtering by month... ")
        popular_month=df1['month'].mode()[0]
        print('Most Popular Month:', popular_month)
        popular_month_name=calendar.month_name[popular_month]
        print('Most Popular Month Name:', popular_month_name)
    if day=='all':
        # extract DAY OF THE WEEK from the Start Time column to create an hour column
        print("Since we are not filtering by day.... ")
        df1['dow'] = df1['Start Time'].dt.weekday_name
        popular_weekday_name=df1['dow'].mode()[0]
        print('Most Popular day of the week:', popular_weekday_name, '\n')
       

   
####### 2. POPULAR STATIONS OF TRIP##########################
    common_start_st=df1['Start Station'].mode()[0]
    common_end_st=df1['End Station'].mode()[0]
    print('POPULAR STATIONS OF TRIP STATS')
    print("Common start station:", common_start_st)
    print("Common end station:", common_end_st)
    print("Common start and end station combination:", "\n",df1.groupby(['Start Station','End Station']).size().nlargest(1) , '\n')
    
    
    ###### 3. TRIP DURATION ###########################
    print('DURATION STATS')
    tot_duration=df1['Trip Duration'].sum()
    avg_duration=df1['Trip Duration'].mean()
    print('Total duration:', tot_duration)
    print('Average duration:', avg_duration,'\n')
    
    #checks
    # print (df1['Start Station'].value_counts  
    #print (df1['hour'].value_counts())
    # print('Average duration:', df1['Trip Duration'].describe(),'\n')

################### 4.  USER INFO STATS ##############################

###  User type
def user_stats(df1):
    """
    calculates user statistics for applied filters in city, month and day of the week
    1. different user types with counts of each type
    2. If city is new york or chicago then :
        a. gender types by counts is calculated
        b. DOB stats calculated are: earliest DOB, latest DOB and DOB which has the maximum occurance
    
    Arguments: 
    df1 = dataframe which has beeen created  based on user inputs
    Returns:
    none
    """
    
    print('USER STATS INFO')
    user_types = df1['User Type'].value_counts()
    #df1.groupby(['Start Station','User Type']).size().reset_index(name='counts')
    print(user_types)
   # print(df1.groupby(['Start Station','User Type']).size().reset_index(name='counts'))    


### Gender counts, earliest, most recent, most common year of birth (only available for NYC and Chicago)

def user_stats_gender_DOB(df1,city):
    # print(df1['month'].unique())
   
     if (city== 'chicago' or city =='new york'):
        #gender
            user_gender= df1['Gender'].value_counts()
            print ("Count of each Gender: ", user_gender)
         #most common DOB
            user_dob=df1['Birth Year'].mode()[0]
            user_dob_cnt=df1['Birth Year'].value_counts().max()            
            print ('Most Common DOB:{}, count : {}'.format(int(user_dob), user_dob_cnt))
          # earliest dOB
            user_dob_min=df1['Birth Year'].min()
            print ("Earliest DOB: ",int(user_dob_min))
          #latest DOB
            user_dob_max=df1['Birth Year'].max()
            print ("Latest DOB: ", int(user_dob_max))

     else:
        print ("\n Gender stats and DOB stats not available for the filter criteria selected \n")


def show_data(df1):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    display_data=''
    i=0
    while display_data not in display_response:
        display_data=input("Do you want to see raw data. Please enter yes or no: \n")
        display_data=display_data.lower()
        if display_data=='yes':
            print(df1.head())
        else:
            print("Please enter yes or no")
    while display_data == 'yes':
        display_data=input("Continue loading next 5 records. Enter yes or no? \n")
        i +=5
        rdata = input().lower()
        if display_data == "yes":
             print(df1[i:i+5]) 
        else:
            if display_data != "yes":
              break
 

#Main function 
def main():
    print ("In main")
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_data(df)
        restart_yes_no = input('\nWould you like to restart? Enter yes or no.\n')
        if restart_yes_no.lower() != 'yes':
            break

if __name__ == "__main__":
	main()



