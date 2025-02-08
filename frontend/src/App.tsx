import React, { useState } from 'react';
import { RecordButton } from './components/RecordButton';
import { Transcript } from './components/Transcript';

const App: React.FC = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [transcript, setTranscript] = useState<string>('');
    const [error, setError] = useState<string>('');

    const handleToggleRecording = async () => {
        try {
            const action = isRecording ? 'stop' : 'start';
            const response = await fetch('/api/record', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ action })
            });

            let data;
            try {
                data = JSON.parse(await response.text());
            } catch (parseError) {
                throw new Error('Erreur lors de la lecture de la réponse du serveur');
            }

            if (data.error) {
                throw new Error(data.error);
            }

            if (action === 'stop' && data.transcript) {
                setTranscript(data.transcript);
            }
            setIsRecording(!isRecording);
            setError('');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Erreur lors de l\'enregistrement');
            setIsRecording(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-4xl mx-auto p-6">
                <header className="text-center mb-12">
                    <h1 className="text-3xl font-light text-gray-800 mb-2">
                        Assistant de Consultation Médicale
                    </h1>
                    <p className="text-gray-600">
                        Enregistrement et transcription de consultations médicales
                    </p>
                </header>

                {error && (
                    <div className="mb-8 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
                        <p className="flex items-center">
                            <span className="mr-2">⚠️</span>
                            {error}
                        </p>
                    </div>
                )}

                <div className="bg-white rounded-lg shadow-sm p-8 mb-8 text-center">
                    <RecordButton
                        isRecording={isRecording}
                        onClick={handleToggleRecording}
                    />
                </div>

                <Transcript content={transcript} />
            </div>
        </div>
    );
};

export default App; 