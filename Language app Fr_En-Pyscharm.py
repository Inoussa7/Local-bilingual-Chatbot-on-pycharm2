import os
import openai
import translator as translator
from gtts import gTTS
import pyttsx3
import speech_recognition as sr
import string
import random
from playsound import playsound
import time
openai.api_key = "YOUR_API_KEY_HERE"

def translate(text, target_language):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate '{text}' to {target_language}:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    print(response.choices[0])
    return response.choices[0].text.strip()


# Define greeting keywords
GREETING_KEYWORDS = ['hello', 'hi', 'hey']

# Define the dialogue array
dialogueArray = []

def build_prompt(text, lang):
    if lang == "fr":
        preamble = "Tu t'appelles Ino. Tu es un assistant amical d'apprentissage des langues. Répond en français en 30 mots ou moins à la réponse suivante de l'étudiant: "
    else:
        preamble = "Your name is Ino. You are a friendly language learning assistant. Please respond in 30 words or less to the following student's response: "
    preamble_text = preamble + text
    return preamble_text

# Define function to generate text using OpenAI API
def generate_text(prompt, language):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].text.strip()

    # Translate message to selected language
    if language != 'english':
        message = translator.translate(message, dest=language).text

    return message

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY_HERE"

def generate_response(text, language,processed_text):
    # Define the GPT-3.5 model to use based on language
    if language == "en":
        model = "text-davinci-003"
    elif language == "fr":
        model = "text-davinci-003"
    else:
        model = "text-davinci-003"

    # Generate message using OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=processed_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
        frequency_penalty=0.0,
        presence_penalty=0.0,

    )

    """message = response.choices[0].text.strip()"""
    # Select a random response from the API results
    message = random.choice(response.choices).text.strip()
    return message


def handle_text_input(output_preference, language):
    text = input("You: ").lower()

    processed_text = build_prompt(text, language)

    # Check if input text is a greeting
    for keyword in GREETING_KEYWORDS:
        if keyword in text:
            keyword_map = {'hello': 'Hello!', 'hi': 'Hi there!', 'hey': 'Hey!'}
            response = keyword_map[keyword]

            break
        else:
            #print(processed_text)
            response = generate_response(text, language, processed_text)

    # Translate response to selected language
    if language != 'english':

    # Add the response to the dialogue array
        inoUserPair = {'who': 'Ino', 'response': response}
        dialogueArray.append(inoUserPair)

    if output_preference == 'audio':
        tts = gTTS(response, lang=language)
        tts.save('output.mp3')
        playsound('output.mp3')
    else:
        print(f"Ino: {response}")

def handle_audio_input(output_preference, language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, timeout=5)

    # Recognize speech using Google Speech Recognition
    try:
        user_input = r.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        user_input = "I'm sorry, I could not understand what you said."
    except sr.RequestError as e:
        user_input = "Could not request results from Google Speech Recognition service; {0}".format(e)

    # Translate user input to English for processing
    if language != 'english':
        """user_input = translator.translate(user_input, dest='english').text"""

    # Generate response
    processed_text = build_prompt(user_input, language)
    response = generate_response(user_input, language,processed_text)

    # Output response according to selected preference

    if output_preference == 'audio':
        # Text-to-speech output
        engine = pyttsx3.init()

        if language == 'en':
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')
        elif language == 'fr':
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.thomas')
        else:
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')

        # Say the response only
        engine.say(response)
        engine.runAndWait()

    else:
        # Print output
        print(f"Ino: {response}")


# Initialize speech recognition and translator
r = sr.Recognizer()

def Ino():
    print("Hello, I am Ino, your language learning tutor.")

    # Prompt user for input preference
    while True:
        input_pref = input("Enter 'text' or 'speech' for your input preference: ")
        if input_pref.lower() in ['text', 'speech']:
            break
        else:
            print("Invalid input preference. Please enter 'text' or 'speech'.")

    # Prompt user for language preference
    while True:
        lang_pref = input("Enter 'en' or 'fr' for your language preference: ")
        if lang_pref.lower() in ['en', 'fr']:
            break
        else:
            print("Invalid language preference. Please enter 'en' or 'fr'.")

    # Initialize variable to track whether user wants to continue conversation
    continue_conversation = True

    # Loop for handling user input
    while continue_conversation:
        if input_pref == 'text':
            handle_text_input('text', lang_pref)
        else:
            handle_audio_input('audio', lang_pref)

        # Prompt user to continue or end conversation
        user_input = input("Enter any key to continue or type 'exit' to end conversation: ")
        if user_input.lower() == 'exit':
            continue_conversation = False

if __name__ == "__main__":
    Ino()
