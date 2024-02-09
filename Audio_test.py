from gtts import gTTS
import os

text_to_speak = "Hello, this is another example."

# Create a gTTS object
text_to_speech = gTTS(text=text_to_speak, lang='en')

# Save the audio file
text_to_speech.save("output.mp3")

# Play the audio file
os.system("start output.mp3")

