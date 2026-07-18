import subprocess
import threading
import sounddevice as sd
import numpy as np
import queue
from piper import PiperVoice, SynthesisConfig 
import time 

PIPER_CMD = "piper"
MODEL = "en_US-libritts_r-medium.onnx"
CONFIG = "en_US-libritts_r-medium.onnx.json"

#goodnums = 16,217

SPEAKER = 217  

voice = PiperVoice.load(MODEL, CONFIG)
SAMPLE_RATE = voice.config.sample_rate 

# <-- FIXED: Create a config object required by the new .synthesize() method
synthesis_config = SynthesisConfig(speaker_id=SPEAKER)

speak_queue = queue.Queue()
audio_queue = queue.Queue()
interrupted = False 

def generate_audio(text):
    chunks = []
    for chunk in voice.synthesize(text, synthesis_config):
        chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))
    return np.concatenate(chunks) if chunks else np.array([], dtype=np.int16)

def speak_worker():
    global interrupted
    next_audio = None
    next_text = None

    while True:
        if next_audio is not None:
            audio = next_audio
            next_audio = None
        else:
            text = speak_queue.get()
            if text is None:
                break
            interrupted = False
            audio = generate_audio(text)
            speak_queue.task_done()

        if interrupted:
            with speak_queue.mutex:
                speak_queue.queue.clear()
            next_audio = None
            continue

        def pregenerate():
            nonlocal next_audio, next_text
            try:
                next_text = speak_queue.get(timeout=2)
                next_audio = generate_audio(next_text)
            except queue.Empty:
                pass

        t = threading.Thread(target=pregenerate, daemon=True)
        t.start()

        sd.play(audio, SAMPLE_RATE)
        sd.wait()
        if interrupted:
            with speak_queue.mutex:
                speak_queue.queue.clear()
            next_audio = None  
            t.join()
            continue

        t.join()

        if next_audio is not None:
            speak_queue.task_done()

speak_thread = threading.Thread(target=speak_worker, daemon=True)
speak_thread.start()

def speak_async(text: str):

    if text.strip():
        speak_queue.put(text)

def speak_stream(text: str):
    if not text.strip():
        return
    global interrupted
    interrupted = False
    audio = generate_audio(text)
    sd.play(audio, SAMPLE_RATE)
    sd.wait()
    if interrupted:
        with speak_queue.mutex:
            speak_queue.queue.clear()

# Run the test
#speak_stream('HELLO sir, i hope you are having a great day')


