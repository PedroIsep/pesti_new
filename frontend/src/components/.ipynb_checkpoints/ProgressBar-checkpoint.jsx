import React, { useState, useEffect } from 'react';

export default function Progressbar({ isRunning }) {
    const [filled, setFilled] = useState(0);

    useEffect(() => {
        let interval;
        if (isRunning && filled < 100) {
            interval = setInterval(() => {
                setFilled(prev => Math.min(prev + 1, 100));
            }, 100); // 100ms interval for 25 seconds duration
        } else if (!isRunning) {
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [isRunning, filled]);

    return (
        <div>
            <div className="progressbar" style={{ visibility: filled === 100 ? 'hidden' : 'visible' }}>
                <div style={{
                    height: "100%",
                    width: `${filled}%`,
                    backgroundColor: "navy",
                    transition: "width 0.1s" // Transition matches the interval
                }}></div>
                <span className="progressPercent">{filled}%</span>
            </div>
        </div>
    );
}