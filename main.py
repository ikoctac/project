import speech_recognition as sr
import os
from datetime import datetime
from functions import *
from mapping import map_text_to_asl_images, display_images_sequentially  # importing necessary functions from the secondary program.

# init recognizer.
recognizer = sr.Recognizer()

# define current speaker.
current_speaker = "person 1"

# get the current directory of the script.
current_directory = os.path.dirname(os.path.abspath(__file__))

# directory path where you save the CSV file.
directory_path = os.path.join(current_directory, "csv_files")

# use the default microphone as source, bot asks what language will the user speak and then prompt the available languages.
with sr.Microphone() as source:
    speak_language_prompt() # bot asks user what will he use(Function is in seperate py file.)
    language = select_language()
    print(f"Listening in {language}...")

    # create the csv_filename
    csv_filename = os.path.join(directory_path, f"speech_data_{language}.csv")

    # adjust for ambient noise if necessary.
    recognizer.adjust_for_ambient_noise(source)

    # continuously listen for speech.
    while True:
        try:
            # Capture audio.
            audio = recognizer.listen(source)

            # convert speech to text using the selected language.
            text = recognizer.recognize_google(audio, language=language)

            # get timestamp for csv refference.
            timestamp = datetime.now().strftime("%H:%M:%S")

            # save the data to CSV file with speaker identifier.
            save_to_csv(csv_filename, timestamp, text, current_speaker)

            # map text to ASL images.
            asl_images = map_text_to_asl_images(text, language)

            # print what the user said.
            print(f"{current_speaker} said:", text)

            # display ASL images sequentially.
            display_images_sequentially(asl_images)

            # check for switch commands.
            if check_switch_command(text, language) :
                print("Switch command detected. Who is speaking?")
                new_speaker = input("Enter the new speaker (e.g., Person 2): ")
                current_speaker = new_speaker
                print(f"Switched to {new_speaker}")

            # check for termination phrase.
            elif check_termination_phrase(text, language):
                speak_termination_prompt()
                decision = input("Do you want to terminate the process? (yes/no): ")
                if decision.lower() == 'yes':
                    print("Terminating the process.")
                    break  # Exit the loop
                else:
                    print("Resuming...")
                    
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error fetching results; {0}".format(e))
