"""
@author Barnabas Vizy
Inserts a tweet_obj into the MySQL database.
To config the database:
    > CREATE TABLE reminders(
    -> sender varchar(15) NOT NULL,
    -> hour INT NOT NULL,
    -> minute INT NOT NULL,
    -> period varchar(4) NOT NULL,
    -> time_zone varchar(20) NOT NULL,
    -> month tinyint NOT NULL,
    -> day tinyint NOT NULL,
    -> msg varchar(123) NOT NULL,
    -> following bit NOT NULL);
"""

import pymysql
from twitter import Twitter, OAuth
from datetime import *
import time
from error import update_log
from random import randint


auth = OAuth(
    consumer_key='2CE1E6U7odFK1MFWeCnOPIh5R',
    consumer_secret='SqqWIvcMGdLbwAqu2oSBzsCr4379aSITLy4AsA9HZyPQxYqCl6',
    token='796842527487889409-hY298XB4dZGxBLU2blhpCVMz14UPQo8',
    token_secret='E9CmwGNpDNffxzU7NjuXernjofYSEF6RyjEKiVantXJap'
)
# auth = OAuth(  # keys for reminderbot002@gmail.com , secondary test account with same login
#     consumer_key='PfV0xdYWs55kstAO4PHF1kIHt',
#     consumer_secret='wYtyvj7EaHBWftLCR8sfYBJKQISu4PhhWszIuLACo0I4jqBgAi',
#     token='792039779068157952-HxKthF9JlcGtDYEiHfT1bn456tJKNLE',
#     token_secret='Fl24QTmnau3vQB3svxDBnepwTL4ifGHvLJVD52PXKXh99'
# )

t = Twitter(auth=auth)

while (1<2):
    conn = pymysql.connect(host='localhost', user='root', passwd='thisisthepassword', db='thereminderbot')
    cursor = conn.cursor()
    # query for selecting ALL table records
    query = ("SELECT SENDER, HOUR, MINUTE, PERIOD, TIME_ZONE, MONTH, DAY, MSG, FOLLOWING FROM reminders ")
    # cursor is now full table
    cursor.execute(query)
    print("Checking DB...")
    # for every element in table, do any of the times match
    # if they do, send tweet to user with message
    for (SENDER, HOUR, MINUTE, PERIOD, TIME_ZONE, MONTH, DAY, MSG, FOLLOWING) in cursor:

        tweet_string = "Hey @" + SENDER + " - " + MSG + " - " + str(randint(1000, 9999))
        timeEST = datetime.now()

        militarytimefix = 0
        if(PERIOD == "PM"):
            militarytimefix = 12

        newtime = timeEST.hour-militarytimefix
        if newtime < 0 :
            newtime = timeEST.hour

        current_time = datetime(timeEST.year, timeEST.month, timeEST.day, newtime, timeEST.minute, 0)
        #print("HOUR:"+str(HOUR)+", MIN: "+str(MINUTE)+", MONTH:"+str(MONTH)+", DAY: "+str(DAY)+", "+str(current_time))
        if MONTH == timeEST.month and DAY == current_time.day and HOUR == current_time.hour and MINUTE == timeEST.minute:
            print("SENDER: {0}, HOUR: {1}, MINUTE: {2}, PERIOD: {3}, TIME_ZONE: {4}, MONTH: {5}, DAY: {6}, MSG: {7}, FOLLOWING: {8}".format(SENDER, HOUR, MINUTE, PERIOD, TIME_ZONE, MONTH, DAY, MSG, FOLLOWING))
            #use twitter connection to send reminder
            t.statuses.update(status=str(tweet_string))
            update_log(SENDER, "Reminder completed")
            #remove all reminders by user after successful expiration of most recent reminder
            cursor.execute("DELETE FROM reminders WHERE sender = '"+SENDER+"'")
            #commiting changes to db is absolutely essential
            conn.commit()
            time.sleep(1.0) #wait a second so we don't send out a million tweets at once
            continue

    time.sleep(60.0)
    conn.close()
    cursor.close()