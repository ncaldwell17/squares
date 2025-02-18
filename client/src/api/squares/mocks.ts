import type {Square} from '@/api/squares/model.ts';

export const squares: Square[] = [
    {
        id: crypto.randomUUID(),
        color: '#FF0000', // red
        rotation: 45
    },
    {
        id: crypto.randomUUID(),
        color: '#00FF00', // green
        rotation: 90
    },
    {
        id: crypto.randomUUID(),
        color: '#0000FF', // blue
        rotation: 180
    }
];