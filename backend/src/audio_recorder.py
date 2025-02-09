import os
import sounddevice as sd
import numpy as np
import soundfile as sf
from datetime import datetime

class AudioRecorder:
    def __init__(self, output_dir="recordings"):
        # Query default input device
        device_info = sd.query_devices(kind='input')
        print(f"Using input device: {device_info['name']}")
        
        self.RATE = int(device_info['default_samplerate'])
        self.CHANNELS = min(device_info['max_input_channels'], 2)
        self.output_dir = output_dir
        self.is_recording = False
        self.frames = []
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def start_recording(self):
        self.frames = []
        self.is_recording = True
        
        def callback(indata, frames, time, status):
            if status:
                print(f"Status: {status}")
            if self.is_recording:
                self.frames.append(indata.copy())
        
        self.stream = sd.InputStream(
            samplerate=self.RATE,
            channels=self.CHANNELS,
            dtype=np.float32,
            callback=callback
        )
        self.stream.start()
        print(f"Recording started... (Using {self.CHANNELS} channel{'s' if self.CHANNELS > 1 else ''} at {self.RATE}Hz)")
        
    def stop_recording(self):
        if hasattr(self, 'stream'):
            self.is_recording = False
            self.stream.stop()
            self.stream.close()
            
            if self.frames:
                recording = np.concatenate(self.frames, axis=0)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/consultation_{timestamp}.wav"
                
                sf.write(filename, recording, self.RATE)
                print(f"Recording saved to {filename}")
                return filename
            
        return None 