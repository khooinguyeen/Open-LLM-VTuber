import os
import requests
import json
import time
from pathlib import Path
from tts_interface import TTSInterface

class TTSEngine(TTSInterface):
    def __init__(
            self, 
            voice="s3://voice-cloning-zero-shot/ea58fa16-2b04-4042-883e-02018079eb9f/au-tenaage-voice/manifest.json",
            user_id="aBmeEqyT4Abe6wNaiTGaAX7xCx82", 
            secret_key="16f2234ed3c3447f819869eeddc7f687"):
        self.voice = voice
        self.user_id = user_id  # Replace with your PlayHT User ID
        self.secret_key = secret_key  # Replace with your PlayHT Secret Key
        self.temp_audio_file = "temp"
        self.file_extension = "mp3"
        self.new_audio_dir = "temp"

        if not os.path.exists(self.new_audio_dir):
            os.makedirs(self.new_audio_dir)

    def generate_audio(self, text, file_name_no_ext=None):
        file_name = file_name_no_ext or f"temp_{int(time.time())}"  # Include timestamp for uniqueness
        file_path = str(Path(self.new_audio_dir) / f"{file_name}.{self.file_extension}")

        headers = {
            "accept": "text/event-stream",
            "content-type": "application/json",
            "authorization": f"{self.secret_key}",
            "x-user-id": f"{self.user_id}"
        }

        payload = {
            "text": text,
            "voice": self.voice,
            "output_format": "mp3",
            "voice_engine": "PlayHT2.0",
            "temperature": 2,
            "emotion": "female_happy"
        }

        response = requests.post("https://api.play.ht/api/v2/tts", json=payload, headers=headers, stream=True)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.json()}")
            return None

        audio_url = None
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                event_data = line.decode('utf-8')
                print(f"Received line: {event_data}")  # Debugging line

                # Check if "event: completed" is in the line
                if "event: completed" in event_data:
                    # Prepare to capture the next line for the audio URL
                    continue  # Skip this line to get the next line
                    
                # Check if "event: generating" or "event: completed" was received
                if "data: " in event_data:
                    # Extract the audio URL from the JSON data
                    data_start = event_data.find("data: ")
                    audio_data = event_data[data_start + len("data: "):]
                    audio_info = json.loads(audio_data)
                    audio_url = audio_info.get("url")
                    print(f"Audio URL: {audio_url}")  # Debugging line

        if not audio_url:
            print("Error: No audio URL received")
            return None

        # Download the audio file
        audio_response = requests.get(audio_url)
        if audio_response.status_code != 200:
            print(f"Error downloading audio: {audio_response.status_code}, {audio_response.text}")
            return None

        with open(file_path, 'wb') as f:
            f.write(audio_response.content)

        return file_path

if __name__ == "__main__":
    tts = TTSEngine()
    file_path = tts.generate_audio("This is just a test script.")
    if file_path:
        print(f"Audio saved to {file_path}")