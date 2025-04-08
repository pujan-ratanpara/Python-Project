import openai
import speech_recognition as sr
import pyttsx3
import os
import subprocess
import psutil
import webbrowser

# Set up OpenAI API Key
openai.api_key = "your_openai_api_key"  # Replace with a valid OpenAI API key

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def configure_tts_engine():
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)  # Female voice
    engine.setProperty("rate", 150)

configure_tts_engine()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            user_input = recognizer.recognize_google(audio)
            print(f"You: {user_input}")
            return user_input.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Error with the speech recognition service.")
            return ""
        except sr.WaitTimeoutError:
            speak("Listening timed out.")
            return ""

def chat_with_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Sorry, I couldn't process your request. Please try again later."

def open_application(app_name):
    """Open applications or websites by name."""
    try:
        app_name = app_name.lower()

        # Web Services
        if "youtube" in app_name:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")
        elif "google" in app_name:
            webbrowser.open("https://www.google.com")
            speak("Opening Google.")
        elif "gmail" in app_name:
            webbrowser.open("https://mail.google.com")
            speak("Opening Gmail.")
        elif "facebook" in app_name:
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook.")
        elif "twitter" in app_name:
            webbrowser.open("https://www.twitter.com")
            speak("Opening Twitter.")
        elif "github" in app_name:
            webbrowser.open("https://www.github.com")
            speak("Opening GitHub.")
        elif "stack overflow" in app_name:
            webbrowser.open("https://stackoverflow.com")
            speak("Opening Stack Overflow.")
        elif "maps" in app_name:
            webbrowser.open("https://www.google.com/maps")
            speak("Opening Google Maps.")

        # Local Applications
        elif "notepad" in app_name:
            subprocess.Popen(["notepad.exe"])
            speak("Opening Notepad.")
        elif "calculator" in app_name or "calc" in app_name:
            subprocess.Popen(["calc.exe"])
            speak("Opening Calculator.")
        elif "paint" in app_name:
            subprocess.Popen(["mspaint.exe"])
            speak("Opening Paint.")
        elif "file explorer" in app_name or "explorer" in app_name:
            subprocess.Popen(["explorer.exe"])
            speak("Opening File Explorer.")
        elif "chrome" in app_name:
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.exists(chrome_path):
                subprocess.Popen([chrome_path])
                speak("Opening Google Chrome.")
            else:
                speak("Chrome not found.")
        elif "cmd" in app_name or "command prompt" in app_name:
            subprocess.Popen(["cmd.exe"])
            speak("Opening Command Prompt.")
        elif "settings" in app_name:
            subprocess.Popen(["start", "ms-settings:"], shell=True)
            speak("Opening Settings.")
        elif "control panel" in app_name:
            subprocess.Popen(["control.exe"])
            speak("Opening Control Panel.")
        elif "task manager" in app_name:
            subprocess.Popen(["taskmgr.exe"])
            speak("Opening Task Manager.")
        else:
            speak(f"I don't know how to open {app_name}.")
    except Exception as e:
        speak("Unable to open the application.")

def close_application(app_name):
    try:
        for process in psutil.process_iter(attrs=["name"]):
            if app_name.lower() in process.info["name"].lower():
                process.terminate()
                speak(f"Closing {app_name}.")
                return
        speak(f"{app_name} is not running.")
    except Exception as e:
        speak("Failed to close the application.")

def search_online(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the results for {query}.")

def write_code(language, task):
    prompt = f"Write a {language} program for: {task}"
    code = chat_with_chatgpt(prompt)
    file_name = f"{language}_task_code.txt"
    with open(file_name, "w") as file:
        file.write(code)
    speak(f"Generated code for {task} in {language}. Saved as {file_name}.")
    print(code)

def handle_command(command):
    if "open" in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)
    elif "close" in command:
        app_name = command.replace("close", "").strip()
        close_application(app_name)
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        search_online(query)
    elif "write a code" in command:
        parts = command.split(" in ")
        if len(parts) == 2:
            language_task = parts[1].strip().split(" about ", 1)
            if len(language_task) == 2:
                language, task = language_task
                write_code(language.strip(), task.strip())
                return
        speak("I didn't understand the code request.")
    else:
        response = chat_with_chatgpt(command)
        print(f"AI Bot: {response}")
        speak(response)

def chatbot():
    speak("Hello! I'm your AI assistant. How can I assist you?")
    while True:
        command = listen()
        if "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day!")
            break
        handle_command(command)

# Run the chatbot
chatbot()