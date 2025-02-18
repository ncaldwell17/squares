import React, { useState } from 'react';
import { squares as initialSquares } from "@/api/squares/mocks.ts";
import type { Square } from '@/api/squares/model.ts';

export default function SquaresContainer(): React.ReactElement {
    const [squares, setSquares] = useState<Square[]>(initialSquares);
    const [selectedSquareId, setSelectedSquareId] = useState<string>('');

    const handleRotate = () => {
        setSquares(squares.map(square => {
            if (square.id === selectedSquareId) {
                return {
                    ...square,
                    rotation: square.rotation + 45
                };
            }
            return square;
        }));
    };

    const selectedSquare = squares.find(square => square.id === selectedSquareId);

    return (
        <div className="p-8 bg-gray-100 min-h-screen">
            {/* Squares Visualization */}
            <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4 text-gray-800">Squares Visualization</h2>
                <div className="flex flex-wrap gap-6 justify-center items-center bg-white p-8 rounded-lg shadow-md">
                    {squares.map((square) => (
                        <div
                            key={square.id}
                            onClick={() => setSelectedSquareId(square.id)}
                            className={`w-32 h-32 transition-all duration-300 hover:scale-110 cursor-pointer
                                ${square.id === selectedSquareId ? 'ring-4 ring-blue-500' : ''}`}
                            style={{
                                backgroundColor: square.color,
                                transform: `rotate(${square.rotation}deg)`
                            }}
                        />
                    ))}
                </div>
            </div>

            {/* Rotation Form */}
            <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-800">Rotate Square</h2>
                <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
                    <div>
                        <label htmlFor="square-select" className="block text-sm font-medium text-gray-700 mb-2">
                            Select a Square
                        </label>
                        <select
                            id="square-select"
                            value={selectedSquareId}
                            onChange={(e) => setSelectedSquareId(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">Choose a square...</option>
                            {squares.map((square) => (
                                <option key={square.id} value={square.id}>
                                    Square ({square.color})
                                </option>
                            ))}
                        </select>
                    </div>

                    {selectedSquare && (
                        <div className="flex items-center justify-between">
                            <div
                                className="w-16 h-16 transition-transform duration-300"
                                style={{
                                    backgroundColor: selectedSquare.color,
                                    transform: `rotate(${selectedSquare.rotation}deg)`
                                }}
                            />
                            <button
                                type="button"
                                onClick={handleRotate}
                                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                            >
                                Rotate 45°
                            </button>
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
}