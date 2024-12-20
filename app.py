import streamlit as st
import pandas as pd
from helper import scrape_comments, analyze_sentiments

# Streamlit UI
st.title("Video Comment Sentiment Analysis")
st.markdown("### Enter a YouTube video link for analysis")

video_link = st.text_input("YouTube Video Link")

if st.button("Analyze Comments"):
    if "youtube.com" in video_link or "youtu.be" in video_link:
        try:
            video_id = video_link.split("v=")[-1].split("&")[0] if "v=" in video_link else video_link.split("/")[-1]
            comments = scrape_comments(video_id)
            
            if comments:
                analysis_results = analyze_sentiments(comments)
                df = pd.DataFrame(analysis_results)
                st.success(f"Analyzed {len(comments)} comments successfully!")
                st.dataframe(df)
                st.divider()
                st.bar_chart(df['sentiment'].value_counts())
            else:
                st.warning("No comments found!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please provide a valid YouTube video link.")
