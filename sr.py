import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak your passphrase for authentication:")
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print("Speech recognized:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        return None

def authenticate_user(expected_passphrase="open sesame"):
    passphrase = recognize_speech()
    if passphrase and passphrase.lower() == expected_passphrase.lower():
        print("Authentication successful. Access granted.")
        return True
    else:
        print("Authentication failed. Access denied.")
        return False

if __name__ == "__main__":
    authenticate_user()
