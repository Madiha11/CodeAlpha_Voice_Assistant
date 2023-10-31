import pyttsx3
import requests
import speech_recognition as sr
import difflib
from datetime import datetime

api_key = '849b554a03544b5f171dfe98bb3c9cdd'

commands = ["how are you", "weather report", "exit"]

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print("You said: " + query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not request results; check your network connection.")
        return ""

def get_best_match(query, commands):
    matches = difflib.get_close_matches(query, commands, n=1, cutoff=0.5)
    if matches:
        return matches[0]
    else:
        return None

def get_weather(city):
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    if api_data["cod"] == 200:
        temp_city = ((api_data['main']['temp']) - 273.15)
        weather_desc = api_data['weather'][0]['description']
        hmdt = api_data['main']['humidity']
        wind_spd = api_data['wind']['speed']
        return f"The weather in {city} is {weather_desc} with a temperature of {temp_city:.2f}°C. Humidity: {hmdt}%, Wind Speed: {wind_spd} kmph."
    else:
        return "Weather information not available."

def main():
    while True:
        command = recognize_speech()
        if command == "":
            print("Command not recognized. Please try again.")
        else:
            best_match = get_best_match(command, commands)
            if best_match:
                if best_match == "exit":
                    print("Exiting the voice assistant.")
                    speak("Exiting the voice assistant.")
                    break
                elif best_match == "how are you":
                    print("I'm good, thank you!")
                    speak("I'm good, thank you!")
                elif best_match == "weather report":
                    speak("Please enter the city for weather information: ")
                    city = input("Please enter the city for weather information: ")
                    speak(city)
                    weather_info = get_weather(city)
                    print(weather_info)
                    speak(weather_info)
            else:
                print("Command not recognized. Please try again.")
                speak("Command not recognozed. Please try again.")

if __name__ == "__main__":
    main()
        