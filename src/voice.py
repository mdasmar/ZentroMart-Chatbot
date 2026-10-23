from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient
from src.retreiver import respond
from dotenv import load_dotenv
load_dotenv()
thread_id = "1"
stt = GnaniSTTClient() 
tts = GnaniTTSClient()
def STT(audio_path):
    heard = stt.transcribe(audio_path, language_code="en-IN")["transcript"]
    if not heard.strip():
        reply = "Sorry, I didn't catch that. Could you say it again?"
    return heard

def TTS(heard):
    reply = respond(heard) 
    tts.synthesize(reply['answer'], voice="Kaveri", model="timbre-v2.5",language="en-IN", output_file="sample_reply/reply.wav")
    return reply['answer']

