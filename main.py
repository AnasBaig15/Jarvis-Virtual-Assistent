import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
import difflib

recognizer = sr.Recognizer()

newsapi = os.getenv("NEWS_API_KEY", "")

USER_NAME = "Anas"


# ---------------- FEMALE VOICE ----------------

def speak(text):
    print("Friday:", text)

    try:
        engine = pyttsx3.init()

        engine.setProperty("volume", 1.0)
        engine.setProperty("rate", 150)

        voices = engine.getProperty("voices")

        for voice in voices:
            voice_info = (
                str(voice.name) + " " +
                str(voice.id) + " " +
                str(getattr(voice, "gender", ""))
            ).lower()

            if any(name in voice_info for name in [
                "zira", "female", "hazel",
                "susan", "aria", "jenny"
            ]):
                engine.setProperty("voice", voice.id)
                break

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Voice error:", repr(e))


# ---------------- MUSIC PLAYER ----------------

def playMusic(song_name):
    song_name = song_name.lower().strip()

    # Normalize music library keys
    songs = {
        name.lower().strip(): link
        for name, link in musicLibrary.music.items()
    }

    # Exact match
    if song_name in songs:
        speak(f"Playing {song_name}")
        webbrowser.open(songs[song_name])
        return

    # Partial match
    for name, link in songs.items():
        if song_name in name or name in song_name:
            speak(f"Playing {name}")
            webbrowser.open(link)
            return

    # Similar name matching
    matches = difflib.get_close_matches(
        song_name,
        songs.keys(),
        n=1,
        cutoff=0.5
    )

    if matches:
        matched_song = matches[0]
        speak(f"Playing {matched_song}")
        webbrowser.open(songs[matched_song])
    else:
        speak(f"Sorry, I could not find {song_name} in your music library.")
        print("Available songs:", list(songs.keys()))


# ---------------- PROCESS COMMAND ----------------

def processCommand(command):
    command = command.lower().strip()

    print("Processing command:", command)

    # Greetings
    if "hello" in command:
        speak(f"Hello {USER_NAME}! How can I help you?")

    # USER NAME
    elif (
        "what is my name" in command
        or "what's my name" in command
        or "tell me my name" in command
        or "do you know my name" in command
    ):
        speak(f"Your name is {USER_NAME}.")

    # FRIDAY NAME
    elif "your name" in command:
        speak("My name is Friday, your personal assistant.")

    elif "how are you" in command:
        speak(f"I am doing great, {USER_NAME}. Thank you for asking!")

    # WEBSITES
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    # MUSIC COMMANDS
    elif command.startswith("play "):
        song = command.replace("play ", "", 1).strip()

        if song:
            playMusic(song)
        else:
            speak("Please tell me which song you want to play.")

    elif command.startswith("play song "):
        song = command.replace("play song ", "", 1).strip()
        playMusic(song)

    # NEWS
    elif "news" in command:
        try:
            if not newsapi:
                speak("Please configure your News API key.")
                return True

            url = "https://newsapi.org/v2/everything"

            params = {
                "q": "Pakistan",
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 5,
                "apiKey": newsapi
            }

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])

                if articles:
                    speak("Here are the latest news headlines.")

                    for article in articles:
                        title = article.get("title")

                        if title and title != "[Removed]":
                            speak(title)
                else:
                    speak("Sorry, no news articles were found.")
            else:
                print(
                    "News API error:",
                    response.status_code,
                    response.text
                )
                speak("Sorry, I could not fetch the news.")

        except requests.RequestException as e:
            print("News request error:", repr(e))
            speak("I am unable to connect to the news service.")

    # STOP FRIDAY
    elif command in [
        "stop", "exit", "quit", "stop friday"
    ]:
        speak(f"Goodbye {USER_NAME}! Friday is shutting down.")
        return False

    else:
        speak("Sorry, I don't understand that command.")

    return True


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    speak(f"Initializing Friday. Welcome back {USER_NAME}.")

    while True:
        try:
            with sr.Microphone(device_index=1) as source:
                print("Listening for wake word Friday...")

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = recognizer.recognize_google(audio)

            print("You said:", word)

            if "friday" in word.lower():

                # Allow direct commands:
                # "Friday play Safar"
                command = word.lower().split("friday", 1)[1].strip()

                if not command:
                    speak(f"Yes {USER_NAME}, I am listening.")

                    with sr.Microphone(device_index=1) as source:
                        print("Friday active. Speak your command...")

                        audio = recognizer.listen(
                            source,
                            timeout=10,
                            phrase_time_limit=7
                        )

                    command = recognizer.recognize_google(audio)

                print("Command:", command)

                if not processCommand(command):
                    break

        except sr.WaitTimeoutError:
            print("No speech detected. Try again.")

        except sr.UnknownValueError:
            print("Sorry, I could not understand.")

        except sr.RequestError as e:
            print("Speech recognition error:", e)

        except KeyboardInterrupt:
            print("\nFriday stopped.")
            break

        except Exception as e:
            print("Error:", repr(e))
