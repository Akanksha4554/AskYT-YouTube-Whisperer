# AskYT-YouTube-Whisperer
**AskYT: Unlock Insights from YouTube Videos 🎥**   AskYT transforms YouTube content into actionable insights. Summarize transcripts, perform sentiment analysis, and engage in Q&amp;A with AI-powered precision. Featuring multi-language support, speech-to-text, and PDF export, it’s your ultimate tool for interactive learning and analysis!

# AskYT 🎥: Transforming YouTube Videos into Actionable Insights with Q&A 📚💡

AskYT is an AI-powered tool designed to transform YouTube videos into actionable insights. By leveraging advanced transcript processing, sentiment analysis, and Q&A features, AskYT enables users to extract key points, understand context, and interact with video content meaningfully.

---

## 📖 About AskYT

AskYT helps users make the most of YouTube content by summarizing transcripts, analyzing sentiments, and providing tailored question-and-answer support. Powered by **Google Gemini 2.0 Flash Exp**, the app is perfect for researchers, students, and professionals looking to gain quick insights from lengthy videos.  

---

## 🤔 Why AskYT?

1. **Save Time**: Quickly summarize videos without watching the entire content.
2. **Interactive Learning**: Ask targeted questions based on video transcripts.
3. **Custom Insights**: Generate short or detailed summaries to match your preferences.
4. **User-Friendly Interface**: Intuitive web interface built using **Streamlit**.
5. **Multi-language Support**: Extract and process transcripts in multiple languages, including English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Hindi (hi), Marathi (mr), Gujarati (gu), Telugu (te).
6. 
---

## 🚀 Features

- **Transcript Summarization**: Generate short or detailed summaries of YouTube transcripts.
- **Q&A System**: Ask questions about video content and receive AI-generated answers.
- **Sentiment Analysis**: Assess the tone of the video content with **VADER Sentiment Analysis**.
- **Speech-to-Text Input**: Ask questions using voice recognition.
- **PDF Export**: Download summaries and Q&A history as a structured PDF.
- **Multi-language Support**: Extract transcripts in various languages for broader applicability.

---

## 📁 File Overview

- **`main.py`**: Core application logic for transcript extraction, summarization, Q&A, and sentiment analysis.
- **`requirements.txt`**: Specifies the Python libraries and dependencies.
- **`.env`**: Stores sensitive environment variables, such as the Google API Key.

---

## 🛠️ Setup Instructions  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/Akanksha4554/askyt.git  
   cd askyt  
   ```  

2. **Install Dependencies**:  
   Install the required libraries using:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Configure the Environment**:  
   Update `.env` with your **Google API Key**:
   ```plaintext
   GOOGLE_API_KEY = "Your_API_KEY"
   ```  

4. **Run the Application**:  
   Launch the app using Streamlit:  
   ```bash  
   streamlit run main.py  
   ```  

5. **Start Exploring**:  
   Enter a YouTube link, select transcript language, and let AskYT summarize and analyze the video.

---

## 🛡️ Requirements  

- Python 3.8+  
- Supported platforms: macOS, Linux, Windows  

---

## 📚 Dependencies  

This project relies on:  

- **Streamlit**: For creating the user interface.  
- **YouTube Transcript API**: To extract transcripts from YouTube videos.  
- **Google Generative AI**: For transcript summarization and Q&A.  
- **VADER Sentiment Analysis**: For understanding the tone of transcripts.  
- **FPDF**: To export summaries and Q&A history as PDFs.  
- **SpeechRecognition and PyAudio**: To enable voice input for questions.

For the full list, refer to [`requirements.txt`](requirements.txt).

---

## 🌟 Key Functions  

- **Transcript Summarization**: Extract and summarize YouTube video transcripts efficiently.  
- **Interactive Q&A**: Ask questions about the content and get AI-driven responses.  
- **Sentiment Analysis**: Understand the mood or tone of the video content.  
- **Multi-language Support**: Process transcripts in diverse languages for global accessibility.  
- **PDF Export**: Compile the summary and Q&A history into a downloadable format.  

---

## 🤝 Contributions  

We welcome contributions to improve AskYT! Feel free to:  
1. Fork the repository.  
2. Create a new branch for your feature or bug fix.  
3. Submit a pull request for review.
---
  
## 📜 License  

This project is licensed under the **MIT License**. You’re free to use, modify, and distribute the software under the terms of the license. Refer to the [LICENSE](LICENSE) file for more details.  

--- 
