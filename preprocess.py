import re
import pandas as pd
def preprocess(data)->pd.DataFrame:
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    try:
        df['message_date'] = pd.to_datetime(df['message_date'],format = "%d/%m/%y, %I:%M\u202f%p - ")
    except:
        df['message_date'] = pd.to_datetime(df['message_date'],format = "%d/%m/%Y, %I:%M\u202f%p - ")
    df.rename(columns={'message_date' : 'date'},inplace=True)
    users = []
    messages = []
    i = 0
    for message in df['user_message']:
        entry = re.split('^(.+?):\s',message)
        if entry[1:]:    #Username
            if "changed the group name from " in entry[1]:
                users.append('notification')
                messages.append(message)
            else:
                users.append(entry[1])
                messages.append(entry[2])
        else :
            users.append('notification')
            messages.append(entry[0])
    df = df.drop(columns="user_message")
    df['user'] = users
    del users
    df['message'] = messages
    del messages
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['date_of_monthh'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['week_day'] = df['date'].dt.weekday
    return df
