import streamlit as st
import openai
import os
import speech_recognition as sr
import warnings

warnings.filterwarnings("ignore")

# Add the access key generated from your OpenAI account
openai.api_key = "openai key"

def chatgpt_api(input_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    if input_text:
        messages.append(
            {"role": "user", "content": 'Summarize this text "{}" into a short and concise Dall-e2 prompt'.format(input_text)},
        )
        
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    
    reply = chat_completion.choices[0].message.content
    return reply

def dall_e_api(dalle_prompt, size="512x512"):
    dalle_response = openai.Image.create(
        prompt=dalle_prompt,
        size=size
    )
    image_url = dalle_response['data'][0]['url']
    return image_url

def whisper_transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak into the microphone...")
        audio = r.listen(source)
        st.write("Audio captured.")
        
    try:
        text = r.recognize_google(audio)
        st.write("Transcribed Text:", text)
        dalle_prompt = chatgpt_api(text)
        image_url = dall_e_api(dalle_prompt, size="256x256")
        st.image(image_url)
    except sr.UnknownValueError:
        st.write("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        st.write("Could not request results from Google Speech Recognition service; {0}".format(e))

st.title("Generate Images using Voice")
whisper_transcribe()
