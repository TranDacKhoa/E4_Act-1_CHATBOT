from pathlib import Path
from openai import OpenAI
import pygame 
from pathlib import Path

def transcribe_text(answer):
    client = OpenAI(api_key="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")
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="fable",
        input=answer,)
    response.stream_to_file(speech_file_path)

def play_mp3(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        sound = pygame.mixer.Sound(str(file_path))
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))  
    except pygame.error as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()


