import React, { useState, useEffect } from 'react';

export default function Progressbar({ isRunning, step }) {
    const [filled, setFilled] = useState(0);
    const [visible, setVisible] = useState(true); 
    
    useEffect(() => {
        let interval;
        if (isRunning && filled < 100 && step == 9.9) { //for images
            interval = setInterval(() => {
                setFilled(prev => Math.min(prev + step, 99));
            }, 1000); 
        } else if (isRunning && filled < 100 && step == 1) { //for videos
            interval = setInterval(() => {
                setFilled(prev => Math.min(prev + step, 99));
            }, 1200); 
        } else if (!isRunning) {
            clearInterval(interval);
            if (filled === 99) {
                setTimeout(() => setVisible(false), 500); 
            }
        }
        return () => clearInterval(interval);
    }, [isRunning, filled]);

    useEffect(() => {
        if (!isRunning && filled < 99) {
            setVisible(true);
        }
    }, [isRunning]);
    
    return (
        <div>
            <div className="progressbar" style={{ visibility: visible ? 'visible' : 'hidden' }}>
                <div style={{
                    height: "100%",
                    width: `${filled}%`,
                    backgroundColor: "navy",
                    transition: "width 0.2s" // Transition matches the interval
                }}></div>
                <span className="progressPercent">{Math.round(filled)}%</span>
            </div>
        </div>
    );
}