# PDAI-A2 - YouTube Video Summarizer

*Effortlessly extract insights and summaries from YouTube videos*

## Overview

The **Smart YouTube Video Summarizer** is an interactive web application that automatically retrieves YouTube video transcripts, generates a detailed, professional multi-section summary, and allows users to engage in an open-ended conversation with an AI chatbot about the video content. This tool is ideal for researchers, educators, and professionals who need to quickly digest lengthy video material.

## Features

- **Automated Transcript Retrieval:**  
  Uses the `youtube-transcript-api` to fetch transcripts directly from YouTube.

- **Structured Summaries:**  
  Generates multi-section summaries including:
  - **Title**
  - **Time Interval**
  - **Summary (bullet points)**
  - **Insights Based on Numbers**
  - **Example Exploratory Questions**

- **Interactive Chatbot:**  
  Engage in a natural conversation with an AI assistant powered by OpenAI and LangChain. The chatbot remains context-aware by retaining the video transcript and summary throughout the conversation.

- **Professional UI:**  
  Built with Streamlit and enhanced with custom CSS, the application features a modern, responsive, and user-friendly interface.

- **Session Persistence:**  
  Maintains the generated summary and conversation history so you can continue your exploration without losing context.

## Utility

The prototype helps users:
- **Save Time:** Quickly grasp key insights without watching the entire video.
- **Enhance Learning:** Deepen understanding through interactive Q&A.
- **Boost Productivity:** Streamline research and information retrieval for professional and academic use.

## Technologies Used

- **Python** – Core programming language
- **Streamlit** – Web application framework
- **LangChain & OpenAI** – For generating high-quality summaries and powering the conversational AI
- **youtube-transcript-api** – To automatically fetch video transcripts
- **Custom CSS** – For an enhanced and professional user interface

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
   cd REPO-NAME
2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
3. **Activate the Virtual Environment:**
    - On Windows:
    ```bash
    venv\Scripts\activate
    - On macOS/Linux::
    ```bash
    source venv/bin/activate
4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
5. **Configure Environment Variables:**
   - Create a .env file in the root directory and add your OpenAI API key:
    ```bash
    OPENAI_API_KEY=your_api_key_here

## Usage
1. **Run the Application:**
   ```bash
   streamlit run app.py
2. Generate a Summary:
   - Enter a YouTube video link.
   - Select the desired summary length (short, medium, or long).
   - Click "Get Transcript and Summary" to generate a structured summary that remains visible.
3. Chat with the AI:
   - Use the persistent chat interface to ask open-ended questions about the video.
   - The chatbot leverages the video transcript and summary to provide contextually relevant responses.
