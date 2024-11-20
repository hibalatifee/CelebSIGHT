import os
from openai import OpenAI
import base64
import json
import time
import simpleaudio as sa
import streamlit as st
import errno
import cv2
import time
from PIL import Image
import numpy as np
from elevenlabs import generate, play, set_api_key, voices
set_api_key(os.environ["ELEVENLABS_API_KEY"])
#set_api_key("134993a2ff0e8b929f49745f2a71a107")

client = OpenAI(api_key='sk-proj-uxUWHARafivIVhTW2L7KT3BlbkFJ6649IDGoQ0JdplIK5hao')

def page_0():
    st.write("# Welcome to CelebSIGHT! 👋")

    st.markdown(
        """
        CelebSIGHT is an open-source web app built to tap into the world of AI, 
      python   voice cloning and image processing.

        **👈 Select a character from the dropdown on the left** to see how 
        they narrate your life in real-time! Let's go...
    """
    )

def page_1():

    def encode_image(image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    # Not a "file in use" error, re-raise
                    raise
                # File is being written to, wait a bit and retry
                time.sleep(0.1)


    def play_audio(text):
        audio = generate(text, voice="TXH8EFI8rq4B7eNPYnOi") #David Attenborough voice

        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        #with open(file_path, "rb") as f:
        #    data = f.read()
        #    b64 = base64.b64encode(data).decode()
        #    md = f"""
        #       <audio controls autoplay="true">
        #       <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        #        </audio>
        #        """
        #    st.markdown(
        #        md,
        #        unsafe_allow_html=True,
        #    )

        #play(audio) # previously used without streamlit
            
        st.audio(audio) # with streamlit without autoplay 


    def generate_new_line(base64_image):
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ]


    def analyze_image(base64_image, script):
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                    Make it snarky and funny. Don't repeat yourself. Make it brief. If I do anything remotely interesting, make a big deal about it!  
                    """,
                },
            ]
            + script
            + generate_new_line(base64_image),
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        return response_text

    script = []

    # path to your image
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # analyze posture
    #print("👀 David is watching you...")
    st.write("👀 David is watching you...")
    analysis = analyze_image(base64_image, script=script)

    #print("🎙️ David says:")
    st.write("🎙️ David says:")
    #print(analysis)
    st.write(analysis)
                
    play_audio(analysis) # works without streamlit as well

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    #time.sleep(5)


def page_2():

    def encode_image(image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    # Not a "file in use" error, re-raise
                    raise
                # File is being written to, wait a bit and retry
                time.sleep(0.1)


    def play_audio(text):
        audio = generate(text, voice="CzHgqaGYUHopBlY7Qc8M", model="eleven_multilingual_v2") #Zia voice

        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        #with open(file_path, "rb") as f:
        #    data = f.read()
        #    b64 = base64.b64encode(data).decode()
        #    md = f"""
        #       <audio controls autoplay="true">
        #       <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        #        </audio>
        #        """
        #    st.markdown(
        #        md,
        #        unsafe_allow_html=True,
        #    )

        #play(audio) # previously used without streamlit
            
        st.audio(audio) # with streamlit without autoplay 


    def generate_new_line(base64_image):
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ]


    def analyze_image(base64_image, script):
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Zia Mohyeddin. 
                    Narrate the picture of the human as if it is a poetry.
                    Make it snarky, rhyming, and funny. Don't repeat yourself. Make it brief. If I do anything remotely interesting, make very romantic!  
                    """,
                },
            ]
            + script
            + generate_new_line(base64_image),
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        return response_text

    script = []

    # path to your image
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # analyze posture
    st.write("👀 Zia is watching you...")
    analysis = analyze_image(base64_image, script=script)

    st.write("🎙️ Zia says:")
    #print(analysis)
    st.write(analysis)
                
    play_audio(analysis) # 

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    #time.sleep(5)

def page_3():

    def encode_image(image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    # Not a "file in use" error, re-raise
                    raise
                # File is being written to, wait a bit and retry
                time.sleep(0.1)


    def play_audio(text):
        audio = generate(text, voice="oWnx3mbsWLPEelS5OODM", model="eleven_multilingual_v2") #Amitabh KBC voice

        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        #with open(file_path, "rb") as f:
        #    data = f.read()
        #    b64 = base64.b64encode(data).decode()
        #    md = f"""
        #       <audio controls autoplay="true">
        #       <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        #        </audio>
        #        """
        #    st.markdown(
        #        md,
        #        unsafe_allow_html=True,
        #    )

        #play(audio) # previously used without streamlit
            
        st.audio(audio) # with streamlit without autoplay 


    def generate_new_line(base64_image):
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ]


    def analyze_image(base64_image, script):
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    Address the human in front of you in the voice of Mr. Amitabh Bachchan as the host of Kaun Banega Crorepati in Hindi. 
                    Talk in Hindi Sanskrit scripture. Make it funny and snarky. 
                    Infuse the interactioans with the person infront of you with encouragement, occasional humor, and profound reflections, mirroring the engaging atmosphere of the show. 
                    Call for applause at the end.  
                    """,
                },
            ]
            + script
            + generate_new_line(base64_image),
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        return response_text
    
    script = []

    # path to your image
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # analyze posture
    st.write("👀 Amit jee is watching you...")
    analysis = analyze_image(base64_image, script=script)

    st.write("🎙️ Amit jee says:")
    #print(analysis)
    st.write(analysis)
                
    play_audio(analysis) # 

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    #time.sleep(5)

def page_4():

    def encode_image(image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    # Not a "file in use" error, re-raise
                    raise
                # File is being written to, wait a bit and retry
                time.sleep(0.1)


    def play_audio(text):
        audio = generate(text, voice="l1c4zvqubk2O5OyDGSBi", model="eleven_multilingual_v2") #Imran Khan voice

        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        #with open(file_path, "rb") as f:
        #    data = f.read()
        #    b64 = base64.b64encode(data).decode()
        #    md = f"""
        #       <audio controls autoplay="true">
        #       <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        #        </audio>
        #        """
        #    st.markdown(
        #        md,
        #        unsafe_allow_html=True,
        #    )

        #play(audio) # previously used without streamlit
            
        st.audio(audio) # with streamlit without autoplay 


    def generate_new_line(base64_image):
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ]


    def analyze_image(base64_image, script):
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    Address the human infront of you in the voice of Imran Khan addressing a political jalsa crowd in Urdu. Talk in Urdu scripture. Capture his charisma, passion, and vision for the nation, weaving in themes of justice, accountability, and progress. Incorporate motivational anecdotes, references to national pride, and appeals for unity and change. Use language that resonates with the audience, employing colloquial expressions and persuasive rhetoric to inspire and mobilize the crowd towards his political agenda.
                    """,
                },
            ]
            + script
            + generate_new_line(base64_image),
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        return response_text
    
    script = []

    # path to your image
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # analyze posture
    st.write("👀 Imran Khan is watching you...")
    analysis = analyze_image(base64_image, script=script)

    st.write("🎙️ Imran Khan says:")
    #print(analysis)
    st.write(analysis)
                
    play_audio(analysis) # 

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    #time.sleep(5)

def page_5():

    def encode_image(image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    # Not a "file in use" error, re-raise
                    raise
                # File is being written to, wait a bit and retry
                time.sleep(0.1)


    def play_audio(text):
        audio = generate(text, voice="CTaR185CKPWxm5RoFtPn", model="eleven_multilingual_v2") #Dora voice

        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        #with open(file_path, "rb") as f:
        #    data = f.read()
        #    b64 = base64.b64encode(data).decode()
        #    md = f"""
        #       <audio controls autoplay="true">
        #       <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        #        </audio>
        #        """
        #    st.markdown(
        #        md,
        #        unsafe_allow_html=True,
        #    )

        #play(audio) # previously used without streamlit
            
        st.audio(audio) # with streamlit without autoplay 


    def generate_new_line(base64_image):
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            },
        ]


    def analyze_image(base64_image, script):
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    Address the human in front of you in the voice of Mr. Shahrukh Khan as the Hindi Bollywood actor in Hindi. 
                    Talk in Hindi Sanskrit scripture. Quote dialogues from romantic Bollywood movies. 
                    Make it very romantic and lovey-dovey.
                    """,
                },
            ]
            + script
            + generate_new_line(base64_image),
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        return response_text
    
    script = []

    # path to your image
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # analyze posture
    st.write("👀 SRK is watching you...")
    analysis = analyze_image(base64_image, script=script)

    st.write("🎙️ SRK says:")
    #print(analysis)
    st.write(analysis)
                
    play_audio(analysis) # 

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    #time.sleep(5)

PAGES = {
    "CelebSIGHT": page_0,
    "David Attenborough":page_1,
    "Zia Mohyeddin": page_2,
    "Amitabh Bachchan": page_3,
    "Imran Khan": page_4,
    "SRK": page_5
}

def main():
    st.sidebar.title('Navigation')
    choice=st.sidebar.selectbox("Select your character", list(PAGES.keys()))
    PAGES[choice]()


#You are Shahrukh Khan. Narrate the picture of the human in Urdu as if it is a Bollywood movie.
#Make it snarky, and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make it seem funny!

if __name__ == "__main__":
    main()
