

# # 2016 US Bike Share Activity Snapshot

# ## Introduction
# 
# > **Tip**: Quoted sections like this will provide helpful instructions on how to navigate and use a Jupyter notebook.
# 
# Over the past decade, bicycle-sharing systems have been growing in number and popularity in cities across the world. Bicycle-sharing systems allow users to rent bicycles for short trips, typically 30 minutes or less. Thanks to the rise in information technologies, it is easy for a user of the system to access a dock within the system to unlock or return bicycles. These technologies also provide a wealth of data that can be used to explore how these bike-sharing systems are used.
# 
# In this project, you will perform an exploratory analysis on data provided by [Motivate](https://www.motivateco.com/), a bike-share system provider for many major cities in the United States. You will compare the system usage between three large cities: New York City, Chicago, and Washington, DC. You will also see if there are any differences within each system for those users that are registered, regular users and those users that are short-term, casual users.


# ## Data Collection and Wrangling
# 
# Now it's time to collect and explore our data. In this project, we will focus on the record of individual trips taken in 2016 from our selected cities: New York City, Chicago, and Washington, DC. Each of these cities has a page where we can freely download the trip data.:
# 
# - New York City (Citi Bike): [Link](https://www.citibikenyc.com/system-data)
# - Chicago (Divvy): [Link](https://www.divvybikes.com/system-data)
# - Washington, DC (Capital Bikeshare): [Link](https://www.capitalbikeshare.com/system-data)
# 
# If you visit these pages, you will notice that each city has a different way of delivering its data. Chicago updates with new data twice a year, Washington DC is quarterly, and New York City is monthly. **However, you do not need to download the data yourself.** The data has already been collected for you in the `/data/` folder of the project files. While the original data for 2016 is spread among multiple files for each city, the files in the `/data/` folder collect all of the trip data for the year into one file per city. Some data wrangling of inconsistencies in timestamp format within each city has already been performed for you. In addition, a random 2% sample of the original data is taken to make the exploration more manageable. 
# 
## import all necessary packages and functions.
import csv # read and write csv files
from datetime import datetime # operations to parse dates
from pprint import pprint # use to print data structures like dictionaries in
                          # a nicer way than the base print function.

def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))
    
    with open(filename, 'r') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)
        
        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        first_trip = next(trip_reader)
        
        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##
        pprint(first_trip)
    
    # output city name and first trip for later testing
    return (city, first_trip)
    

# list of files for each city
data_files = ['./data/NYC-CitiBike-2016.csv',
              './data/Chicago-Divvy-2016.csv',
              './data/Washington-CapitalBikeshare-2016.csv',]

# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip


datum = {}
def duration_in_mins(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.
    
    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds. 
    
    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """
    
    if city == 'NYC':
        duration = int(datum['tripduration']) /60
    elif city == 'Chicago':
        duration = int(datum['tripduration']) /60
    else:
        duration = int(datum['Duration (ms)']) /60000
    return duration


def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.
    
    Remember that NYC includes seconds, while Washington and Chicago do not.
    
    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    if city == 'NYC':        
        d1 = datetime.strptime((datum['starttime']), "%m/%d/%Y %H:%M:%S")
        month = int(d1.strftime("%m"))
        hour = int(d1.strftime("%H"))
        day_of_week=d1.strftime("%A")
          
    elif city =='Chicago':
        d2 = datetime.strptime((datum['starttime']), "%m/%d/%Y %H:%M")
        month = int(d2.strftime("%m"))
        hour = int(d2.strftime("%H"))
        day_of_week=d2.strftime("%A")
        
    else:
        d3 = datetime.strptime((datum['Start date']), "%m/%d/%Y %H:%M")
        month = int(d3.strftime("%m"))
        hour = int(d3.strftime("%H"))
        day_of_week=d3.strftime("%A")    
        
    return (month, hour, day_of_week)


def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.
    
    Remember that Washington has different category names compared to Chicago
    and NYC. 
    """
    
    if city =='NYC':
        user_type = str(datum['usertype'])
    elif city == 'Chicago':
        user_type = str(datum['usertype'])
    else:
        if datum['Member Type'] == "Registered":
            user_type = 'Subscriber'
        else:
            user_type = 'Customer'
            
    return user_type


def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.
    
    HINT: See the cell below to see how the arguments are structured!
    """
    import csv
    with open(out_file, 'w') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']        
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()
        
        ## TODO: set up csv DictReader object ##
        trip_reader = list(csv.DictReader(f_in)) 

        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            new_point = {}
            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            new_point['duration'] = duration_in_mins(row,city)
            new_point['month'] = time_of_trip(row,city)
            new_point['week'] = time_of_trip(row,city)
            new_point['day_of_week'] = time_of_trip(row,city)
            new_point['user_type'] = type_of_user(row,city)

            ## TODO: write the processed information to the output file.     ##
            
            f_out.write("{},".format(new_point['duration']))
            f_out.write("{},".format(new_point['month'][0]))
            f_out.write("{},".format(new_point['week'][1]))
            f_out.write("{},".format(new_point['day_of_week'][2]))
            f_out.write("{}\n".format(new_point['user_type']))


# ## Exploratory Data Analysis
# 
# Now that you have the data collected and wrangled, you're ready to start exploring the data. In this section you will write some code to compute descriptive statistics from the data. You will also be introduced to the `matplotlib` library to create some basic histograms of the data.
# 
# ### Statistics
# 
# **Answer**: NYC has the maximum number of trips, the number is 276798
# NYC has the highest proportion of trips made by subscribers, the percentage is 88.84%
# Chicago has the highest proportion of trips made by customers, the percentage is 23.77%


def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        # initialize count variables
        n_subscribers = 0
        n_customers = 0
        len_subs_ride = 0
        len_cust_ride = 0
        
        # tally up ride types
        for row in reader:
            if row['user_type'] == 'Subscriber':
                n_subscribers += 1
                len_subs_ride += float(row['duration'])
            else:
                n_customers += 1
                len_cust_ride += float(row['duration'])
        
        # compute total number of rides
        n_total = n_subscribers + n_customers
        pct_subs = n_subscribers / n_total
        pct_custs = n_customers / n_total
        
        avg_subs_ride = len_subs_ride/n_subscribers
        avg_cust_ride = len_cust_ride/n_customers
        
        # return tallies as a tuple
        return(n_subscribers, n_customers, n_total, pct_subs, pct_custs, avg_subs_ride, avg_cust_ride)


data_file1 = './data/Washington-2016-Summary.csv'
data_file2 = './data/NYC-2016-Summary.csv'
data_file3 = './data/Chicago-2016-Summary.csv'

list_n_trips = {"Washington":number_of_trips(data_file1)[2],
                "NYC":number_of_trips(data_file2)[2], "Chicago": number_of_trips(data_file3)[2]}
max_n_trips = max(list_n_trips, key=list_n_trips.get)                
print('{} has the maximum number of trips, the number is {}' .format(max_n_trips, list_n_trips[max_n_trips]))

list_subs_pct = {"Washington":number_of_trips(data_file1)[3],
                "NYC":number_of_trips(data_file2)[3], "Chicago": number_of_trips(data_file3)[3]}
max_subs_pct = max(list_subs_pct, key=list_subs_pct.get)                
print('{} has the highest proportion of trips made by subscribers, the percentage is {:.2%}' 
      .format(max_subs_pct, list_subs_pct[max_subs_pct]))

list_cust_pct = {"Washington":number_of_trips(data_file1)[4],
                "NYC":number_of_trips(data_file2)[4], "Chicago": number_of_trips(data_file3)[4]}
max_cust_pct = max(list_cust_pct, key=list_cust_pct.get)                
print('{} has the highest proportion of trips made by customers, the percentage is {:.2%}' 
      .format(max_cust_pct, list_cust_pct[max_cust_pct]))

                
def length_of_trips(filename):
    
    with open(filename, 'r') as f_in:
        # set up csv reader object #
        reader = csv.DictReader(f_in)
        
        n_short = 0
        n_long = 0
        len_short = 0
        len_long = 0
        
        # duration tally #
        for row in reader:
            if float(row['duration']) <=30:
                n_short += 1
                len_short += float(row['duration'])
            else:
                n_long += 1
                len_long += float (row['duration'])
                
        # total number of rides #
        n_total = n_short + n_long
        len_total = len_short + len_long
        
        avg_len = len_total/n_total
        pct_long = n_long/n_total
        pct_short = n_short/n_total
        
        return(len_total, n_total, avg_len, pct_long, pct_short)
    
data_file1 = './data/Washington-2016-Summary.csv'
data_file2 = './data/NYC-2016-Summary.csv'
data_file3 = './data/Chicago-2016-Summary.csv'  

list_len = {"Washingtion":length_of_trips(data_file1)[2],
            "NYC":length_of_trips(data_file2)[2], "Chicago":length_of_trips(data_file3)[2]}
print('The average trip length for {} is {:.2f} (min), the proportion of rides made are longer that 30 mins is {:.2%}'.
      format(list(list_len.keys())[list(list_len.values()).index(length_of_trips(data_file1)[2])],
             length_of_trips(data_file1)[2], length_of_trips(data_file1)[3]))
print('The average trip length for {} is {:.2f} (min), the proportion of rides made are longer that 30 mins is {:.2%}'.
      format(list(list_len.keys())[list(list_len.values()).index(length_of_trips(data_file2)[2])],
             length_of_trips(data_file2)[2], length_of_trips(data_file2)[3]))
print('The average trip length for {} is {:.2f} (min), the proportion of rides made are longer that 30 mins is {:.2%}'.
      format(list(list_len.keys())[list(list_len.values()).index(length_of_trips(data_file3)[2])],
             length_of_trips(data_file3)[2], length_of_trips(data_file3)[3]))



data_file = './data/Washington-2016-Summary.csv'

if number_of_trips(data_file)[5] > number_of_trips(data_file)[6]:
    print ('Subscribers in Washington take longer rides on the average. The average subscriber trip duration is {:.2f}(mins),the average customer trip duration is {:.2f} (mins)'.format(number_of_trips(data_file)[5], number_of_trips(data_file)[6]))
else:
    print ('Customers in Washington take longer rides on the average. The average subscriber trip duration is {:.2f}(mins), the average customer trip duration is {:.2f}(mins)'.format(number_of_trips(data_file)[5], number_of_trips(data_file)[6]))



# ### Visualizations


# load library
import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().run_line_magic('matplotlib', 'inline')

# example histogram, data taken from bay area sample
data = [ 7.65,  8.92,  7.42,  5.50, 16.17,  4.20,  8.98,  9.62, 11.48, 14.33,
        19.02, 21.53,  3.90,  7.97,  2.62,  2.67,  3.08, 14.40, 12.90,  7.83,
        25.12,  8.30,  4.93, 12.43, 10.60,  6.17, 10.88,  4.78, 15.15,  3.53,
         9.43, 13.32, 11.72,  9.85,  5.22, 15.10,  3.95,  3.17,  8.78,  1.88,
         4.55, 12.68, 12.38,  9.78,  7.63,  6.45, 17.38, 11.90, 11.52,  8.63,]
plt.hist(data)
plt.title('Distribution of Trip Durations')
plt.xlabel('Duration (m)')
plt.show()



tripdata = []

def list_triptimes (filename):
    """
    Function that reads trip data and reports the number of trips made
    """
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        #duration tally#
        for row in reader:
            tripdata.append(float(row['duration']))
        return tripdata
        
data_file = './data/Washington-2016-Summary.csv'
bins = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280]

plt.hist(list_triptimes(data_file),bins)
plt.title('Trip Duration - Washington')
plt.xlabel('Duration (mins)')
plt.legend ()
plt.show()
           


subs_data = []
cust_data = []

def list_triptimes(filename):
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        #Ride type tally#
        for row in reader:
            if row['user_type'] == 'Subscriber':
                subs_data.append(float(row['duration']))
            else:
                cust_data.append(float(row['duration']))
        return (subs_data, cust_data)
    
data_file = './data/Washington-2016-Summary.csv'
bins =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]

plt.hist(list_triptimes(data_file)[0],bins,histtype='bar',rwidth=0.8)
plt.title('Subscriber Trip Duration - Washington')
plt.xlabel('Duration (mins)')
plt.legend ()
plt.show()

plt.hist(list_triptimes(data_file)[1],bins,histtype='bar',rwidth=0.8)
plt.title('Customer Trip Duration - Washington')
plt.xlabel('Duration (mins)')
plt.legend ()
plt.show()


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def trip_month(filename):
    
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        fall = [9,10,11]
        winter = [12,1,2]
        spring = [3,4,5]
        summer = [6,7,8]
        
        cnt_subs_fall = 0
        cnt_subs_winter = 0
        cnt_subs_spring = 0
        cnt_subs_summer = 0
        
        cnt_cust_fall = 0
        cnt_cust_winter = 0
        cnt_cust_spring = 0
        cnt_cust_summer = 0
        
        #data conversion#
        for row in reader:
            if row['user_type'] == 'Subscriber':
                if int(row['month']) in fall:
                    cnt_subs_fall += 1
                elif int(row['month']) in winter:
                    cnt_subs_winter += 1
                elif int(row['month']) in spring:
                    cnt_subs_spring += 1
                else:
                    cnt_subs_summer += 1
            else:
                if int(row['month']) in fall:
                    cnt_cust_fall += 1
                elif int(row['month']) in winter:
                    cnt_cust_winter += 1
                elif int(row['month']) in spring:
                    cnt_cust_spring += 1
                else:
                    cnt_cust_summer += 1
                    
        fall_ratio = cnt_subs_fall/cnt_cust_fall
        winter_ratio = cnt_subs_winter/cnt_cust_winter
        spring_ratio = cnt_subs_spring/cnt_cust_spring
        summer_ratio = cnt_subs_summer/cnt_cust_summer
        
        fall_total = cnt_subs_fall+cnt_cust_fall
        winter_total = cnt_subs_winter+cnt_cust_winter
        spring_total = cnt_subs_spring+cnt_cust_spring
        summer_total = cnt_subs_summer+cnt_cust_summer
        
        subs_season = {"Fall": cnt_subs_fall,"Winter": cnt_subs_winter,"Spring": cnt_subs_spring,"Summer": cnt_subs_summer}
        cust_season = {"Fall": cnt_cust_fall,"Winter": cnt_cust_winter,"Spring": cnt_cust_spring,"Summer": cnt_cust_summer}
        ratio_season = {"Fall":fall_ratio,"Winter":winter_ratio,"Spring":spring_ratio,"Summer":summer_ratio}
        total_season = {"Fall":fall_total,"Winter":winter_total,"Spring":spring_total,"Summer":summer_total}
        
        return subs_season,cust_season,ratio_season,total_season
    
data_file1 = './data/Washington-2016-Summary.csv'
data_file2 = './data/NYC-2016-Summary.csv'
data_file3 = './data/Chicago-2016-Summary.csv' 


subs_season1,cust_season1,ratio_season1,total_season1 = trip_month(data_file1) #Washington Season Data#
max1 =max(total_season1, key=total_season1.get)
max_subs1 = max(subs_season1, key=subs_season1.get)
print("For Washington, highest ridership is during {}, {}. {} has the highest subscriber ridership at {}" .format(max1, total_season1[max1], max_subs1, subs_season1[max_subs1]))

subs_season2,cust_season2,ratio_season2,total_season2 = trip_month(data_file2) #NYC Season Data#
max2 =max(total_season2, key=total_season2.get)
max_subs2 = max(subs_season2, key=subs_season2.get)
print("For NYC, highest ridership is during {}, {}. {} has the highest subscriber ridership at {}" .format(max2, total_season2[max2], max_subs2, subs_season2[max_subs2]))

subs_season3,cust_season3,ratio_season3,total_season3 = trip_month(data_file3) #Chicago Season Data#
max3 =max(total_season3, key=total_season3.get)
max_subs3 = max(subs_season3, key=subs_season3.get)
print("For Chicago, highest ridership is during {}, {}. {} has the highest subscriber ridership at {}" .format(max3, total_season3[max3], max_subs3, subs_season3[max_subs3]))

#Bar Chart for Customer and Subscriber ridership#

x = [k for k in subs_season3]
y = [v for v in subs_season3.values()]
x_pos = np.arange(len(x))

x2 = [k for k in subs_season3]
y2 = [v for v in subs_season3.values()]
x2_pos = np.arange(len(x2))


plt.bar(x,y,alpha=0.5, label='Subscriber', color = 'y')
plt.bar(x2,y2, alpha=0.5, label='Customer', color = 'g')

plt.title('Customer and Subscriber Ridership Chart')
plt.xlabel('Seasons')
plt.ylabel('Trips')
plt.legend()
plt.show()

x3 = [k for k in ratio_season3]
y3 = [v for v in ratio_season3.values()]
plt.bar(x3,y3,alpha=0.5, label='Ratio' )
plt.title('Subscriber-Customer Trip Ratio')
plt.legend()
plt.show()



from subprocess import call
call(['python', '-m', 'nbconvert', 'Bike_Share_Analysis.ipynb'])

