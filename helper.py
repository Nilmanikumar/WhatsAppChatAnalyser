from urlextract import URLExtract
from wordcloud import WordCloud,STOPWORDS
import pandas as pd
from collections import Counter
import emoji
extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    number_of_messages = df.shape[0]
    words = 0
    num_url = 0
    for messages in df['message']:
        words += len(messages.split())
        num_url += len(extractor.find_urls(messages))

    
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    return number_of_messages,words,num_media,num_url

def most_active_users(df,user_list):
    user_list.remove('Overall')
    count = df['user'].value_counts()[user_list]
    # print(user_list)
    return count

# Word Cloud
def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    text = df['message'].str.cat(sep=' ')
    custom_stopwords = set(STOPWORDS)
    # "null","deleted","message","waiting"
    custom_stopwords.update(["omitted","message","Waiting","Media","null","deleted"])
    wc = WordCloud(width=400 , height=400 , min_font_size=10,background_color=
                   'white',stopwords=custom_stopwords)
    df_wc = wc.generate(text)
    return df_wc
f = open('stop_hinglish.txt','r')
text_stopw = f.read()
f.close()

def get_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['user'] != 'notification']
    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in text_stopw and word not in  ["<Media omitted>\n","<media","omitted>","null","deleted","message","waiting","<this","edited>"]:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20),columns=["words","count"])

def GET_EMOJI(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emoji_list = []
    for message in df['message']:
        emoji_list.extend([c for c in message if c in emoji.EMOJI_DATA])
    return pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))),columns=["emoji","count"])

def get_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['month_num'] = df["date"].dt.month
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] =  time
    return timeline

def get_weekly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['month_num'] = df["date"].dt.month
    timeline  = (df.groupby('week_day').count()['message']).reset_index()
    timeline['day_name'] = timeline['week_day'].map({0:'Monday',1:'Tuesday',2:"Wednesday",3:'Thrusday',4:'Friday',5:'Saturday',6:'Sunday'})
    return timeline

def get_hourly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby('hour').count()['message'].reset_index()
    return timeline


    

    