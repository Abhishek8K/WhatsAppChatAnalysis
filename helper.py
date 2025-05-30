from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()




def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    df_filtered = df[df['users'] != 'group_notification'] 
    x = df_filtered['users'].value_counts().head()
    df = round((df_filtered['users'].value_counts() / df_filtered.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'}) 
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
      df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
      y = []
      for word in message.lower().split():
        if word not in stop_words:
          y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
      emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    df['date'] = pd.to_datetime(df['Message Date'])

    # Extract year, month number, and month name
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')

    timeline = df.groupby(['year','month_num','month_name']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['date'] = pd.to_datetime(df['Message Date'])
    df['only_date'] = df['date'].dt.date

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['date'] = pd.to_datetime(df['Message Date'])  
    df['day_name'] = df['date'].dt.day_name()

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['date'] = pd.to_datetime(df['Message Date'])  # Corrected line
    df['month'] = df['date'].dt.strftime('%B') 

    return df['month'].value_counts()
    
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['date'] = pd.to_datetime(df['Message Date'])
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['period'] = df['hour'].apply(lambda x: f"{x:02d}-{(x+1)%24:02d}")

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap



