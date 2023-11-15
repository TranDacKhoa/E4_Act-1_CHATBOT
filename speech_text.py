from openai import OpenAI
import pyaudio
import threading
import keyboard
import wave


def transcribe_audio(file_path,language="vi"):
    client = OpenAI(api_key="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")
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language=language,
                response_format="text"
            )
            return transcript
    except Exception as e:
        return f"Error: {e}"



def record_audio(file_name):
    audio = pyaudio.PyAudio()
    frames = []
    is_recording = False

    def start_recording():
        nonlocal is_recording
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        while not is_recording:
            pass  

        while is_recording:
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

    threading.Thread(target=start_recording).start()

    input("Start...")
    is_recording = True
    input("End..")

    is_recording = False
