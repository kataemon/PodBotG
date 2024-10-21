import os
import openai
import google.generativeai as genai
GOOGLE_API_KEY = "AIzaSyCuOleS3aaNZAQ03vAHWgPyPo6o9pBqsZ8"
"""from dotenv import load_dotenv"""
from TTS_Really_m import client as ttsclient
import azure.cognitiveservices.speech as speechsdk
from openai import OpenAI
import os
import speech_recognition as sr  # Import speech recognition
import io
import tempfile
import threading

openai.api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"]="sk--koalIjlbxNJykzFNsqvopW7Zez0d2lF8gcAgqdfuCT3BlbkFJqcSeY7beJhaxca1HaqHj4x6unUC2AEwpQHNeJjIssA"
clienty = OpenAI()
a=0
"""def check_space_key():
    while True:
        if keyboard.is_pressed('space'):
            return 1
            break  # Exit after detecting space key
space_thread = threading.Thread(target=check_space_key)
space_thread.start()"""
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            temp_audio_file.write(audio.get_wav_data())
            temp_audio_file.flush()  # Ensure data is written

            # Send the file path to OpenAI Whisper API
            translation = clienty.audio.translations.create(
                model="whisper-1",
                file=open(temp_audio_file.name, "rb")
            )
        print(f"You: {translation.text}")
        return translation.text

    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
"""def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            # Check if 'ctrl' key is pressed to interrupt the loop
            if keyboard.is_pressed('ctrl'):
                print("Ctrl key pressed! Restarting recognition loop...")
                break

            print("Listening...")
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

        except sr.UnknownValueError:
            ttsclient.request_tts_and_play("Sorry, I did not catch that.")
        except sr.RequestError as e:
            ttsclient.request_tts_and_play("Could not request results; {e}")
            return ""
"""
"""def stt():
    # Azure STT API key
    speech_key, service_region = "<your api key>", "eastus"
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region, speech_recognition_language='zh-TW')
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    client = OpenAI()

    audio_file = open("/path/to/file/audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    print(transcription.text)
    print("Say something...")

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.
    result = speech_recognizer.recognize_once()
    """
def load_guideline():
    import PyPDF2

    pdf_file_path = ('./1_PDFsam_splitGuideline-obesity.pdf')
    txt_file_path = 'guideline_processed.txt'  # Path to save the processed text

    pdf_reader = PyPDF2.PdfReader(open(pdf_file_path, 'rb'))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'  # Separate pages with a newline

    # Save the processed text to a .txt file
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    return text
guideline_text=load_guideline()
prompt_uno=f"""
    "Guideline text will be given in the first 'user prompt'"
    "You should be able to retrieve and readily know the chat history"
    "You are PodBot, a conversational assistant specialized in gastrointestinal and liver diseases.",
    "The user is a gastroenterologist in a qualified medical center "
    "User is seeking extensive education on the provided guideline.",
    "Give precise answers and understand the questions of the user clearly and work on that topic do not try to give general knowledge"
    "Adopt a warm, podcast-style tone.",
    "Engage in dynamic conversations, making small talk and asking questions to specify topics.",
    "However, do not repeat yourself and keep in mind the previous conversations.",
    "Provide clear insights from the guidelines, and be ready to evaluate the user's knowledge by asking questions.",
    "Don't use rude words."
    "Please construct full sentences and at least paraphrase from the given text."
"""
# Set model parameters
"""config = GenerationConfig(
    temperature=0.9,
    top_p=1.0,
    top_k=32,
    candidate_count=1,
    max_output_tokens=8192,
)"""


genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash',
system_instruction = [prompt_uno]
)
chat = model.start_chat(history=[])

#System_Prompt = chat.send_message(f"""
#You are PodBot, a conversational assistant specialized in gastrointestinal and liver diseases. The user is a gastroenterologist working in a qualified medical center seeking extensive education on the provided guidelines.

#- Adopt a warm, podcast-style tone.
#- Engage in dynamic conversations, encourage user to specify but still explain thoroughly.
#- Provide clear insights from the guidelines, emphasizing key points.
#- Be ready to evaluate the user's knowledge by asking questions.

#""" + prompt_uno)


# Note that the chat object is temporarily stateful, as you send messages and get responses, you can
# see the history changing by doing chat.history.
a=chat.send_message(f""" please start with "Hello, I am PodBot. I am here to help you understand 'ASGE–ESGE guideline on primary
endoscopic bariatric and metabolic therapies for adults with
obesity'. Do you want me to summarize the document or do you have specific questions?
The guideline text:
{guideline_text}
""")
ttsresponse=ttsclient.request_tts(a.text)
print(a.text)
ttsclient.play_audio(ttsresponse)


# Start conversation loop
while True:
    user_input = listen()

# If user wants to exit the conversation
    if user_input in ["Goodbye.", "Exit", "Quit."]:
        print("PodBot: Goodbye! Have a great day!")
        ttsresponse = ttsclient.request_tts("Goodbye! Have a great day!")
        ttsclient.play_audio(ttsresponse)
        ttsclient.terminate()
        break

        # Generate response from the model
    response = chat.send_message(f"{user_input}")
    ttsresponse=ttsclient.request_tts(response.text)
    print(f"PodBot: {response.text}")
    ttsclient.play_audio(ttsresponse)