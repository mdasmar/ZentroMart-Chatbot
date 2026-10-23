import sounddevice as sd
import soundfile as sf
import numpy as np 


audio_chunks = []
stream = None

def start_recording():
    global audio_chunks, stream
    audio_chunks = []

    def callback(indata, frames, time, status):
        audio_chunks.append(indata.copy())

    stream = sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="int16",
        callback=callback
    )
    stream.start()


def stop_recording():
    global stream

    stream.stop()
    stream.close()

    audio = np.concatenate(audio_chunks, axis=0)
    sf.write("sample_voice/ques.wav", audio, 16000)


def play_audio(audio_file):
    audio, sample_rate = sf.read(audio_file, dtype="float32")

    sd.play(audio, sample_rate)
    sd.wait()