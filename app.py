# app.py
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
from chatbot import ChatBot
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ---------- Custom CSS to enhance UI ----------
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTitle {
        color: #003366;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        padding-bottom: 10px;
    }
    .stSubheader {
        color: #003366;
        font-size: 1.8em;
        font-weight: bold;
        border-bottom: 2px solid #003366;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    .stTextInput > div > input {
        background-color: #ffffff;
        border: 1px solid #ccd6dd;
        border-radius: 4px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #003366;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-size: 1.1em;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #00509e;
    }
    .stForm {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chat-message {
        margin: 10px 0;
        padding: 10px;
        border-radius: 4px;
        background-color: #e9ecef;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def get_video_id(youtube_url: str):
    """Extracts the video ID from a YouTube URL."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    return match.group(1) if match else None

def fetch_transcript(video_id: str):
    """Fetches the transcript of a YouTube video using the video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry['text'] for entry in transcript_list])
        return transcript
    except Exception as e:
        st.error(f"Error retrieving transcript: {e}")
        return None

def get_structured_summary(transcript: str, summary_length: str):
    """
    Generates a multi-section, professional summary:
    1) Title
    2) Time Interval
    3) Summary
    4) Insights Based on Numbers
    5) Example Exploratory Questions

    No commands section. This matches your expectations.pdf style more closely.
    """
    prompt = f"""
You are an expert summarizer. Produce a structured summary with these sections:
1) Title
2) Time Interval (approx range of the transcript)
3) Summary (bullet points)
4) Insights Based on Numbers
5) Example Exploratory Questions (like E1, E2, E3)

Use a {summary_length} summary style. Here is the transcript:

{transcript}
"""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.6, openai_api_key=os.getenv("OPENAI_API_KEY"))
    return llm.predict(prompt)

def main():
    st.title("Smart YouTube Video Summarizer")

    # Input for YouTube link and summary length
    youtube_url = st.text_input("Enter YouTube video link:")
    summary_length = st.radio("Select summary length:", ["short", "medium", "long"])

    # Button to fetch transcript & produce structured summary
    if st.button("Get Transcript and Summary"):
        video_id = get_video_id(youtube_url)
        if not video_id:
            st.error("Invalid YouTube link!")
        else:
            with st.spinner("Fetching transcript..."):
                transcript = fetch_transcript(video_id)
            if transcript:
                with st.spinner("Generating structured summary..."):
                    summary = get_structured_summary(transcript, summary_length)
                
                # Save transcript & summary in session state
                st.session_state.transcript = transcript
                st.session_state.summary = summary

    # If we have a summary, display it
    if "summary" in st.session_state and st.session_state.summary:
        st.subheader("Video Summary")
        st.write(st.session_state.summary)

    # If we have a transcript, show chat
    if "transcript" in st.session_state and st.session_state.transcript:
        st.subheader("Chat with me about the video")
        st.write("What can I help you with now? Ask anything about the video content!")

        # Initialize chat history if needed
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = StreamlitChatMessageHistory(key="history")

        # Instantiate ChatBot
        chatbot = ChatBot(st.session_state.transcript, st.session_state.chat_history)

        # Chat form
        with st.form(key="chat_form"):
            user_query = st.text_input("Your question or comment:")
            submit_query = st.form_submit_button("Send")
            
            if submit_query and user_query.strip():
                with st.spinner("Thinking..."):
                    response = chatbot.get_response(user_query)
                # Add user and AI messages to chat
                st.session_state.chat_history.add_user_message(user_query)
                st.session_state.chat_history.add_ai_message(response)

        # Display conversation history
        if st.session_state.chat_history.messages:
            st.subheader("Conversation History")
            for msg in st.session_state.chat_history.messages:
                st.chat_message(msg.type).write(msg.content)

if __name__ == "__main__":
    main()
