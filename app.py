import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import emoji
import seaborn as sns


st.set_page_config(
    page_title="Whatsapp Chat Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch Unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        
        col1, col2, col3, col4 = st.columns(4)

        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user,df)
        with col1:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Total Messages"}</h1>', unsafe_allow_html=True)
            st.title(num_messages)

        with col2:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Total Words"}</h1>', unsafe_allow_html=True)
            st.title(words)

        with col3:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Media Shared"}</h1>', unsafe_allow_html=True)
            st.title(num_media_messages)
        
        with col4:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Link Shared"}</h1>', unsafe_allow_html=True)
            st.title(links)

        #Monthly timeline
        st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Monthly Timeline"}</h1>', unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #Daily Timeline
        st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Daily Timeline"}</h1>', unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()

        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity Map
        st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Activity Map"}</h1>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Most Busy Day"}</h1>', unsafe_allow_html=True)
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Most Busy Month"}</h1>', unsafe_allow_html=True)
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Activity Heat Map
        st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Weekly Activity Map"}</h1>', unsafe_allow_html=True)
        activity_heat = helper.activity_heat_map(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(activity_heat)
        st.pyplot(fig)
            
        #Finding the busiest users in the (Group level)
        if selected_user == 'Overall':
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Most Busy User"}</h1>', unsafe_allow_html=True)
            x, new_df = helper.most_busy_users(df)

            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Stats"}</h1>', unsafe_allow_html=True)
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Data Frame"}</h1>', unsafe_allow_html=True)
                st.dataframe(new_df)

        #WordCloud
        st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Word Cloud"}</h1>', unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words
        most_common_df = helper.most_common_words(selected_user,df)
        st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Most Common Words"}</h1>', unsafe_allow_html=True)
        fig,ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Stats"}</h1>', unsafe_allow_html=True)
            ax.bar(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Data Frame"}</h1>', unsafe_allow_html=True)
            st.dataframe(most_common_df)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.markdown(f'<h1 style="color:#0DB9CD;font-size:50px;font-weight:800;">{"Emoji Analysis"}</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Data Frame"}</h1>', unsafe_allow_html=True)
            st.dataframe(emoji_df)
        
        with col2:
            st.markdown(f'<h1 style="color:#0DB9CD;font-size:24px;font-weight:500;">{"Stats"}</h1>', unsafe_allow_html=True)
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head())
            st.pyplot(fig)
