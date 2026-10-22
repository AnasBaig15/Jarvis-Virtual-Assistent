
# import speech_recognition as sr

# recognizer = sr.Recognizer()

# # Try the main Realtek microphone
# with sr.Microphone(device_index=1) as source:
#     print("Keep quiet for 2 seconds...")
#     recognizer.adjust_for_ambient_noise(source, duration=2)

#     print("Energy threshold:", recognizer.energy_threshold)
#     print("Speak loudly for 3-5 seconds...")

#     try:
#         audio = recognizer.listen(
#             source,
#             timeout=15,
#             phrase_time_limit=5
#         )

#         print("Audio captured successfully!")

#         with open("test_audio.wav", "wb") as f:
#             f.write(audio.get_wav_data())

#         print("Saved recording to test_audio.wav")

#         try:
#             print("Recognized:", recognizer.recognize_google(audio))
#         except sr.UnknownValueError:
#             print("Audio captured, but speech was not understood.")
#         except sr.RequestError as e:
#             print("Google service error:", e)

#     except sr.WaitTimeoutError:
#         print("No speech detected from microphone index 1.")





# recognizer.adjust_for_ambient_noise(source, duration=0.5)
#                 audio = recognizer.listen(source)

#             command = recognizer.recognize_google(audio)
#             print("You said:", command)

#             # Wake word detection
#             if "jarvis" in command.lower():
#                 speak("Yes, how can I help you?")

#         except sr.UnknownValueError:
#             print("Sorry, I could not understand the audio.")

#         except sr.RequestError as e:
#             print(f"Speech recognition service error: {e}")

#         except OSError as e:
#             print(f"Microphone error: {e}")
#             break

#         except KeyboardInterrupt:
#             print("Jarvis stopped.")
#             break
