import re
import logging
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF
import pyttsx3
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_video_id(url):
    """
    Extract video ID from a YouTube URL.
    """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    else:
        logging.error("Could not extract video ID from the URL. Please check if the URL is valid.")
        return None

def fetch_transcript(video_id):
    """
    Fetch transcript of a given YouTube video ID.
    """
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all text fragments into one transcript
        transcript_text = "\n".join(entry.get('text', '') for entry in transcript_data)
        return transcript_text
    except Exception as e:
        logging.error(f"Error fetching transcript: {e}")
        return None

def save_to_pdf(text, filename="transcript.pdf"):
    """
    Save transcript text to a PDF file with proper formatting.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Use multi_cell for automatic text wrapping
    pdf.multi_cell(0, 10, text)
    
    try:
        pdf.output(filename)
        logging.info(f"Transcript successfully saved as {filename}")
    except Exception as e:
        logging.error(f"Error saving PDF: {e}")

def read_aloud(text):
    """
    Read the transcript text aloud using text-to-speech.
    """
    try:
        engine = pyttsx3.init()
        # Adjust voice and speed settings if necessary
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 25)  # Slightly slower for clearer pronunciation
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Error during reading aloud: {e}")

def main():
    st.title("YouTube to Podcast")
    st.write("Hey user! Enter your YouTube URL, and we will create a PDF of the transcript and provide you with the option to listen to it out loud.")
    
    youtube_url = st.text_input("Enter the YouTube video URL:")
    
    if youtube_url:
        video_id = get_video_id(youtube_url)
        
        if not video_id:
            st.error("Invalid YouTube URL. Please try again.")
        else:
            transcript_text = fetch_transcript(video_id)
            if transcript_text:
                save_to_pdf(transcript_text)
                st.success("Transcript successfully saved as transcript.pdf")
                
                # Provide a download button for the PDF
                with open("transcript.pdf", "rb") as file:
                    st.download_button(
                        label="Download Transcript PDF",
                        data=file,
                        file_name="transcript.pdf",
                        mime="application/pdf"
                    )
                
                # Ask the user if they want the transcript to be read aloud
                if st.button("Read Aloud Transcript"):
                    read_aloud(transcript_text)
                else:
                    st.info("Reading aloud function skipped.")
            else:
                st.error("Could not fetch transcript.")

if __name__ == "__main__":
    main()
