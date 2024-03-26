from gtts import gTTS
from pydub import AudioSegment

def text_to_speech(text, output_file_path, lang='en'):
    # Text-to-speech conversion using gtts
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save the speech as a temporary WAV file
    temp_wav_file = "temp.wav"
    tts.save(temp_wav_file)
    
    # Convert the WAV file to OGG using pydub
    sound = AudioSegment.from_wav(temp_wav_file)
    sound.export(output_file_path, format="ogg")
    
    # Clean up: remove the temporary WAV file
    sound.close()
    cleanup(temp_wav_file)

def cleanup(file_path):
    import os
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up: {e}")

# Example usage
text = "Hello, this is a test message."
output_file_path = "C:\Users\MOHANAPRASAD\SIH23\Telegram\input_voices"

text_to_speech(text, output_file_path)
print(f"Text-to-speech conversion complete. Output saved to {output_file_path}")
