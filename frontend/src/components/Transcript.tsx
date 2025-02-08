import React from 'react';

interface TranscriptProps {
    content: string;
}

export const Transcript: React.FC<TranscriptProps> = ({ content }) => {
    if (!content) return null;

    return (
        <div className="mt-8">
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
                    <h2 className="text-xl font-medium text-gray-800">
                        Transcription de la consultation
                    </h2>
                    <p className="text-sm text-gray-600 mt-1">
                        Dialogue entre le médecin et le patient
                    </p>
                </div>
                <div className="p-6">
                    {content.split('\n').map((line, i) => {
                        const isDoctor = line.startsWith('Médecin:');
                        const isPatient = line.startsWith('Patient:');

                        if (!line.trim()) return null;

                        return (
                            <div
                                key={i}
                                className={`
                                    mb-4 p-3 rounded-lg
                                    ${isDoctor ? 'bg-blue-50 ml-0 mr-12' : ''}
                                    ${isPatient ? 'bg-green-50 ml-12 mr-0' : ''}
                                `}
                            >
                                <div className={`
                                    text-sm font-medium mb-1
                                    ${isDoctor ? 'text-blue-800' : ''}
                                    ${isPatient ? 'text-green-800' : ''}
                                `}>
                                    {isDoctor ? 'Médecin' : 'Patient'}
                                </div>
                                <p className={`
                                    ${isDoctor ? 'text-blue-700' : ''}
                                    ${isPatient ? 'text-green-700' : ''}
                                `}>
                                    {line.replace(/^(Médecin:|Patient:)/, '').trim()}
                                </p>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}; 