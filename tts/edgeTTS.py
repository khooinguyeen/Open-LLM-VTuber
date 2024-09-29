import sys
import os
from pathlib import Path

import edge_tts
from tts_interface import TTSInterface

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


# Check out doc at https://github.com/rany2/edge-tts
# Use `edge-tts --list-voices` to list all available voices


class TTSEngine(TTSInterface):

    def __init__(self, voice="en-US-AvaMultilingualNeural"):
        self.voice = voice

        self.temp_audio_file = "temp"
        self.file_extension = "mp3"
        self.new_audio_dir = "./cache"

        if not os.path.exists(self.new_audio_dir):
            os.makedirs(self.new_audio_dir)

    def generate_audio(self, text, file_name_no_ext=None):
        """
        Generate speech audio file using TTS.
        text: str
            the text to speak
        file_name_no_ext: str
            name of the file without extension


        Returns:
        str: the path to the generated audio file

        """
        file_name = "temp"
        if file_name_no_ext is None:
            file_name = self.temp_audio_file
        else:
            file_name = file_name_no_ext

        file_name = str(Path(self.new_audio_dir) / f"{file_name}.{self.file_extension}")

        try:
            communicate = edge_tts.Communicate(text, self.voice)
            communicate.save_sync(file_name)
        except:
            print(
                "No audio was received. Please verify that your parameters are correct."
            )
            return None

        return file_name


# if __name__ == "__main__":
#     tts = TTSEngine()
#     tts.speak(
#         "Hello World! You no, this is a very interesting phenomenoooooon that somebody is reading this stupid code",
#         lambda: print(">> Start"),
#         lambda: print(">> End"),
#     )

if __name__ == "__main__":
    tts = TTSEngine(voice="en-US-AvaMultilingualNeural")
    file_path = tts.generate_audio("This is a test for EdgeTTS engine.")
    if file_path:
        print(f"EdgeTTS: Audio saved to {file_path}")


# en-US-AvaMultilingualNeural
# en-US-EmmaMultilingualNeural
# en-US-JennyNeural
