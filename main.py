import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from fpdf import FPDF
import io
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # For Sentiment Analysis
import speech_recognition as sr  # For Speech-to-Text
import pyaudio  # Ensure you have pyaudio installed

# Load environment variables
load_dotenv()

# Configure the Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt for summarization
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Function to extract transcript details from YouTube
def extract_transcript_details(youtube_video_url, lang_code='en'):
    try:
        video_id = youtube_video_url.split("=")[1]
        # Attempt to retrieve the transcript for the specified language
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_code])

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript

    except NoTranscriptFound:
        # Handle the case where no transcript is found in the requested language
        st.error(f"No transcript found in {lang_code} for this video.")
        return None
    except TranscriptsDisabled:
        # Handle the case where transcripts are disabled for the video
        st.error("Transcripts are disabled for this video.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Function to generate content using Google Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Sentiment analysis function using VADER
def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    compound_score = sentiment_score['compound']

    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Speech-to-Text function to convert voice input to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for your question... Speak now.")
        audio = recognizer.listen(source)
    try:
        question_text = recognizer.recognize_google(audio)
        st.write(f"Question: {question_text}")  # Display the recognized text
        return question_text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.error("Could not request results from Google Speech Recognition service.")
        return None

# Initialize Streamlit app
st.markdown("""
<div style="text-align: center;">
    <h1>Welcome to AskYT 🎥</h1>
    <h5><i>Transforming YouTube Videos into Actionable Insights with Q&A 📚💡</i></h5>
</div>
""", unsafe_allow_html=True)

# Expander section to describe the app
with st.expander("**About this app**"):
    st.write("""
        AskYT helps you:
        - Summarize YouTube video transcripts with key points.
        - Answer questions based on video content.
        - Get quick insights without watching the entire video.
        - Use Google Gemini 2.0 Flash Exp for precise summaries and answers.
        - Analyze sentiment to understand the mood of the speaker.
    """)

# User input for YouTube URL, language selection, and summary detail level
youtube_link = st.text_input("Enter YouTube Video Link:")
language_code = st.selectbox("Select Language for Transcript", ['en', 'hi', 'mr', 'gu', 'te', 'es', 'fr', 'de', 'it', 'pt'])

# Add slider for summary detail level selection
summary_type = st.selectbox("Select the level of summary detail", ["short", "detailed"])

# Define session state to store video summary and transcript
if 'transcript_text' not in st.session_state:
    st.session_state.transcript_text = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []
if 'summary_displayed' not in st.session_state:
    st.session_state.summary_displayed = False  # Initialize summary_displayed flag

# Define action when the user clicks the "Process Link" button
if st.button("Process Link"):
    if youtube_link:
        try:
            # Extract the transcript details from the YouTube video in the selected language
            transcript_text = extract_transcript_details(youtube_link, language_code)

            if transcript_text:
                # Generate the summary from Google Gemini based on the summary type
                prompt_with_summary_type = prompt + transcript_text + f"\nSummary detail level: {summary_type}"
                summary = generate_gemini_content(transcript_text, prompt_with_summary_type)

                # Get sentiment of the video
                sentiment = get_sentiment(transcript_text)

                # Store the transcript, summary, and sentiment in session state
                st.session_state.transcript_text = transcript_text
                st.session_state.summary = summary

                # Set summary_displayed to True, so the summary will persist
                st.session_state.summary_displayed = True

                # Display the sentiment
                st.markdown(f"### Sentiment: {sentiment}")

                # Display the video history and summary
                st.markdown("## History of Video:")

                # Display the summary at the top
                st.markdown("### Video Summary:")
                st.write(st.session_state.summary)

            else:
                st.error("Unable to extract transcript from the provided video.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display the Video Summary and Q&A History (only if the summary exists)
if st.session_state.summary_displayed:
    # Ensure the summary remains visible after the user submits a question
    st.markdown("### Video Summary:")
    st.write(st.session_state.summary)

    # Ask a question section (allow both text and voice inputs)
    question = st.text_input("Enter your question:")

    if st.button("Ask with Voice"):
        # Capture the question using speech-to-text if the user presses the button
        question = speech_to_text()

    # Automatically process the question as the user presses "Enter"
    if question:
        if not any(qa['question'] == question for qa in st.session_state.qa_history):
            # Answer the question based on the transcript
            qna_prompt = f"Based on the transcript of the YouTube video, answer the following question: {question}"
            answer = generate_gemini_content(st.session_state.transcript_text, qna_prompt)

            # Store question and answer in session state
            st.session_state.qa_history.append({'question': question, 'answer': answer})

            # Display a confirmation message
            st.success(f"Answer for your question '{question}' has been generated.")

    # Display the Q&A history (questions and answers)
    st.markdown("## Q&A History:")
    if st.session_state.qa_history:
        for idx, qa in enumerate(st.session_state.qa_history):
            # Display the question in bold
            st.markdown(f"**Q{idx + 1}: {qa['question']}**")
            # Display the answer normally
            st.write(f"A{idx + 1}: {qa['answer']}")

    # Button to download the summary and Q&A as PDF (triggers the immediate download)
    if st.button("Download Summary and Q&A as PDF"):
        # Create a PDF object
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set title for the PDF
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="YouTube Video Summary and Q&A", ln=True, align='C')

        # Add the video summary to the PDF
        pdf.ln(10)  # Add a line break
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"### Video Summary:\n{st.session_state.summary}\n")

        # Add the Q&A history to the PDF with bold questions
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, "### Q&A History:")

        for idx, qa in enumerate(st.session_state.qa_history):
            # Make the question bold
            pdf.set_font("Arial", size=12, style='B')
            pdf.multi_cell(0, 10, f"Q{idx + 1}: {qa['question']}")
            # Reset font for the answer
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"A{idx + 1}: {qa['answer']}")

        # Save the PDF to a BytesIO object for download
        pdf_output = pdf.output(dest='S').encode('latin1')  # Encoding to avoid issues with non-ASCII characters

        # Trigger the download of the PDF with the same label
        st.download_button(
            label="Download PDF",
            data=pdf_output,
            file_name="summary_and_qa.pdf",
            mime="application/pdf"
        )
