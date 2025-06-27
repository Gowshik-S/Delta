import speech_recognition as sr
import pyttsx3
import pyaudio
import random
import google.generativeai as gen
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from geopy.geocoders import Nominatim
from datetime import datetime

VoA=sr.Recognizer()
eng=pyttsx3.init()

gen.configure(api_key="AIzaSyAUWGgNqvCw7_-z-ve70JF-XCVkcvS5lwA")
ai= gen.GenerativeModel(model_name='models/gemini-1.5-flash-latest')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
client_id= 'c3c73b9a26ae4756ae0d293c079a1ce4',
client_secret=  'bfa7d71cb7ab4b84a506e002839cc50f',
redirect_uri= 'http://127.0.0.1:8888/callback',

scope = "user-library-read user-read-playback-state user-modify-playback-state"))

t_api="VUK4CX097NYW"


def speak(text):
    eng.say(text)
    eng.runAndWait()


def listen():
    with sr.Microphone() as comms:
        VoA.adjust_for_ambient_noise(comms)
        aud = VoA.listen(comms)

        try:
            cmd= VoA.recognize_google(aud)
            if cmd:
                cmd=cmd.lower()
                return cmd
            elif cmd == None :
                return ""
        
        except sr.WaitTimeoutError:
            return "Listening timed out. Please try again"
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand you"
        except sr.RequestError:
            return "Service Unavailabe"

def ai_resp(prmt):
    prmt = f"Answer this briefly as possible: {prmt}"
    try:
        resp=ai.generate_content(prmt)
        return resp.text

    except Exception as e:
            print(f"Error occurred: {e}")
            return "Error generating the response."
    

def pl_sng(name):
    res=sp.search(q=name, type='track', limit=1)
    tracks=res['tracks']['items']

    if not tracks:
        return "Couldn't find the song "
    
    track = tracks[0]
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    track_uri = track['uri']


    sp.start_playback(uris=[track_uri])

    return f"Playing {track_name}."


def get_time(city,t_api):
    lat,lon = geo_lal(city)
    url = f"http://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        'key': t_api,
        'format': 'json',
        'by': 'position',
        'lat': lat,
        'lng': lon
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            time_str = data['formatted']
            time_only = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            return f"The current time in {city} is {time_only}"
        else:
            print(f"API Error: {data['message']}")
            return ""
    except Exception as e:
        print(f"Something went wrong: {e}")
        return ""


def geo_lal(city):
    geoloc = Nominatim(user_agent="time-checker")
    loc = geoloc.geocode(city)
    if loc:
        return loc.latitude, loc.longitude



greet_st=["Hi there! What can I do for you?",
        "Hey, How can I assist you?",
        "Good day! How may I assist you?",
        "Hello, How may i help you?"]

greet=["he","hey", "hey there", "what's up?", 
        "hi hi", "heyy", "holla", "hello", "good day", 
        "greetings", "nice to meet you", "hellooo!", 
        "well hello there!", "hi pal!"]

def get_response(cmd):

    if cmd in greet:
        return random.choice(greet_st)
    elif cmd in "What is your name":
         return "Hai, I am Delta. Your personal Voice Assistant"
         
    elif cmd in ['bye','exit','stop']:
                    return "GoodBye"
    elif cmd.startswith("play"):
                    song=cmd.replace("play","",1).strip()
                    return pl_sng(song)
    elif "time" in cmd:
        if "in" in cmd:
            l = cmd.split("in")
            if len(l) > 1:
                city = l[-1].strip()
        else:
            city="India"                                
        return get_time(city,t_api) 
    elif cmd:
        txt=ai_resp(cmd)
        return txt
    
                
                



    