from openai import OpenAI
from pathlib import Path

class TranscriptionService:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def transcribe(self, audio_file_path):
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="fr",
                    temperature=0.2,
                    response_format="verbose_json",  # Get detailed output with timestamps
                    prompt="Ceci est une consultation médicale entre un médecin et un patient. Veuillez identifier qui parle."
                )
            
            # Process the segments and format as a dialog
            formatted_transcript = ""
            current_speaker = None
            
            for segment in transcript.segments:
                # Simple speaker detection based on patterns
                # This is a basic example - you might want to use more sophisticated detection
                text = segment.text.strip()
                
                # Enhanced French-specific patterns for doctor detection
                is_doctor = any([
                    "?" in text,
                    text.lower().startswith(("comment ", "quand ", "où ", "pourquoi ", "quel", "quelle", "quels", "quelles")),
                    "pouvez-vous" in text.lower(),
                    "pourriez-vous" in text.lower(),
                    "avez-vous" in text.lower(),
                    "décrivez" in text.lower(),
                    "expliquez" in text.lower(),
                    "parlez-moi" in text.lower(),
                    "dites-moi" in text.lower(),
                    "montrez-moi" in text.lower(),
                    "est-ce que" in text.lower(),
                ])
                
                speaker = "Médecin: " if is_doctor else "Patient: "
                
                # Only add speaker label if it changes
                if speaker != current_speaker:
                    formatted_transcript += f"\n{speaker}"
                    current_speaker = speaker
                
                # Add timestamp and text
                timestamp = f"[{int(segment.start)}:{int(segment.end)}] "
                formatted_transcript += f"{timestamp}{text}\n"
            
            return formatted_transcript
            
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None 