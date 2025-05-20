import re
import pandas as pd

def preprocess(data):
  pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s?\u202f?(?:am|pm)\s-\s'
  messages = re.split(pattern, data)[1:]
  dates=re.findall(pattern,data)
  dates = [re.sub(r'\s-\s$', '', re.sub(r'\u202f', '', date))  for date in dates]
  cleaned_dates = pd.to_datetime(dates, format='%m/%d/%y, %I:%M%p')
  cleaned_dates = pd.Series(cleaned_dates)
  cleaned_dates = cleaned_dates.dt.strftime('%d/%m/%Y, %I:%M%p').str.lower() 
  df = pd.DataFrame({
    'User_Message':  messages,
    'Message_Date': cleaned_dates
  })

  df.rename(columns={
    'User_Message': 'User Message',
    'Message_Date': 'Message Date'
  }, inplace=True)
   
  users=[]
  messages=[]
  for message in df['User Message']:
    entry = re.split(r'([\w\W]+?):\s', message)
    
    if entry[1:]:
      users.append(entry[1])
      messages.append(entry[2])
    else:
      users.append('group_notification')
      messages.append(entry[0].strip())

  df['users']=users
  df['message']=messages
  df.drop(columns=['User Message'],inplace=True)
   
  df['Message Date'] = pd.to_datetime(df['Message Date'], format='%d/%m/%Y, %I:%M%p')
  df['month_name'] = df['Message Date'].dt.strftime('%B')  # Full month name
  df['day'] = df['Message Date'].dt.day  # Day of the month
  df['year'] = df['Message Date'].dt.year  # Year
  df['hour'] = df['Message Date'].dt.hour  # Hour (24-hour format)
  df['minute'] = df['Message Date'].dt.minute  # Minute
  return df