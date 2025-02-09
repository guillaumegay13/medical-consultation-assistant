from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from src.audio_recorder import AudioRecorder
from src.transcription import TranscriptionService
import os
from dotenv import load_dotenv

# Initialize Flask with static files configuration
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')

# Configure CORS based on environment
if os.getenv('FLASK_ENV') == 'development':
    CORS(app, origins=['http://localhost:3000'])
else:
    CORS(app, origins=[
        os.getenv('VERCEL_URL'),
        'http://localhost:3000'
    ])

# Load environment variables
load_dotenv()

recorder = AudioRecorder()
transcription_service = TranscriptionService(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(f"Serving path: {path}")  # Debug print
    if path.startswith('api/'):
        return app.view_functions[path]()
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        print(f"Serving static file: {path}")  # Debug print
        return send_from_directory(app.static_folder, path)
    print("Serving index.html")  # Debug print
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/record', methods=['POST'])
def toggle_recording():
    try:
        action = request.json.get('action')
        print(f"Action received: {action}")
        
        if action == 'start':
            recorder.start_recording()
            return jsonify({'status': 'recording', 'message': 'Recording started'})
        
        elif action == 'stop':
            audio_file = recorder.stop_recording()
            if audio_file:
                transcript = transcription_service.transcribe(audio_file)
                if transcript:
                    return jsonify({'status': 'success', 'transcript': transcript})
                return jsonify({'error': 'Transcription error'})
            return jsonify({'error': 'No audio file recorded'})
        
        return jsonify({'error': 'Invalid action'})
    
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 