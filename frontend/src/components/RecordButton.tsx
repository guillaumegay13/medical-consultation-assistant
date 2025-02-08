import React from 'react';

interface RecordButtonProps {
    isRecording: boolean;
    onClick: () => void;
}

export const RecordButton: React.FC<RecordButtonProps> = ({ isRecording, onClick }) => {
    return (
        <div className="flex flex-col items-center">
            <button
                onClick={onClick}
                className={`
                    px-8 py-4 rounded-full font-medium text-lg shadow-md
                    transition-all duration-200 ease-in-out
                    ${isRecording
                        ? 'bg-red-500 hover:bg-red-600 text-white'
                        : 'bg-blue-500 hover:bg-blue-600 text-white'
                    }
                `}
            >
                {isRecording ? "⏹ Arrêter l'enregistrement" : "🎙 Commencer l'enregistrement"}
            </button>
            <p className="mt-2 text-gray-600 text-sm">
                {isRecording
                    ? "L'enregistrement est en cours..."
                    : "Cliquez pour commencer l'enregistrement de la consultation"
                }
            </p>
        </div>
    );
}; 