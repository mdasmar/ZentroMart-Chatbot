from pathlib import Path
import shutil
import argparse
from src.voice import STT, TTS
from src.retreiver import retrieve_context


parser=argparse.ArgumentParser()
parser.add_argument("input_folder", type=Path)
parser.add_argument("--output-dir", type=Path, default=Path("batch_output"))
args=parser.parse_args()

INPUT_FOLDER=args.input_folder
OUTPUT_FOLDER=args.output_dir
OUTPUT_FOLDER.mkdir(exist_ok=True)


for audio_file in sorted(INPUT_FOLDER.glob("*")):

    print(f"Processing: {audio_file.name}")

    transcript = STT(str(audio_file))
    chunks = retrieve_context(transcript)
    reply = TTS(transcript)

    reply_audio=OUTPUT_FOLDER/f"{audio_file.stem}_reply.wav"
    shutil.copy2("sample_reply/reply.wav",reply_audio)

    (OUTPUT_FOLDER/f"{audio_file.stem}_transcript.txt").write_text(transcript, encoding="utf-8")
    (OUTPUT_FOLDER/f"{audio_file.stem}_reply.txt").write_text(reply, encoding="utf-8")
    (OUTPUT_FOLDER/f"{audio_file.stem}_chunks.txt").write_text(chunks, encoding="utf-8")

    print(f"Saved: {reply_audio}")

print("Finished processing all audio files.")