import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
st.set_page_config(
    layout="wide",
    page_title="Chat Analyser",
    page_icon="U+1F4AC"
)
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)
    st.dataframe(df.tail())

    st.title("Statistics")
    #Fetch unique User
    user_list = df['user'].unique().tolist()
    for item in ('notification', 'Meta AI'):
        if item in user_list:
            user_list.remove(item)
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

if st.sidebar.button("Show Analysis"):
    col1,col2,col3,col4 = st.columns(4)
    # Helpher Function ---------------------------------------------
    num_messages,num_words,num_media,num_links = helper.fetch_stats(selected_user,df)
    with col1:
        st.header("Total Messages")
        st.title(num_messages)
    with col2:
        st.header("Total Words")
        st.title(num_words)
    with col3:
        st.header("Media Shared")
        st.title(num_media)
    with col4:
        st.header("Links Shared")
        st.title(num_links)

    # Finding Most Active Users
    if selected_user == 'Overall':
        st.title('Most Active Users')
        # Graph helpher
        x = helper.most_active_users(df,user_list)
        col1,col2 = st.columns(2)
        with col1:
            fig,ax = plt.subplots()
            ax.bar(x.index,x.values,color='red')
            plt.xticks(x.index, rotation=330)
            st.pyplot(fig)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(x.values,labels=x.index,autopct="%1.1f%%")
            st.pyplot(fig)
    col1,col2 = st.columns(2)
    with col1:
        #Word Cloud
        st.title('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig) 
    with col2:
    #Most Used Words
        st.title("Most Common Words")
        word_df = helper.get_words(selected_user,df).sort_values(by = 'count' , ascending=False)
        #plot 
        fig,ax = plt.subplots()
        ax.bar(word_df['words'],word_df['count'])

        # Use an emoji-capable font
        emoji_font = fm.FontProperties(family='Segoe UI Emoji')
        plt.xticks(rotation = 90,fontproperties=emoji_font)
        plt.tight_layout()
        st.pyplot(fig)
    #DF 
    # st.dataframe(word_df)


    #Emoji
    st.title("Emoji's")
    st.dataframe(helper.GET_EMOJI(selected_user,df))

    #TimeLine
    st.title("Monthly Timeline")
    timeline = helper.get_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'])
    plt.xticks(rotation = 90)
    plt.tight_layout()
    st.pyplot(fig) 

    col1,col2 = st.columns(2)
    with col1:
        st.title("Weekly Activity")
        timeline = helper.get_weekly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(timeline['day_name'],timeline['message'],color="green")
        plt.tight_layout()
        plt.xticks(rotation = 90)
        st.pyplot(fig)
    with col2:
        st.title('Hourly TActivity')
        timeline = helper.get_hourly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(timeline['hour'],timeline['message'],color='#F28E2B',edgecolor='#B05E00')
        plt.tight_layout()
        st.pyplot(fig)



