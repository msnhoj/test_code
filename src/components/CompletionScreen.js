import React from 'react';
import './CompletionScreen.css';

const CompletionScreen = ({ onNewSession, onCloseApp }) => {
  return (
    <div className="completion-screen">
      <div className="completion-content">
        <div className="completion-icon">
          <svg viewBox="0 0 100 100" className="checkmark">
            <circle cx="50" cy="50" r="45" fill="none" stroke="#27ae60" strokeWidth="4" />
            <path
              fill="none"
              stroke="#27ae60"
              strokeWidth="6"
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M 25 50 L 42 67 L 75 34"
              className="checkmark-path"
            />
          </svg>
        </div>

        <h1 className="completion-title">MISSION COMPLETE</h1>
        <p className="completion-message">
          You've completed the full deck!<br />
          Outstanding work, soldier.
        </p>

        <div className="completion-stats">
          <div className="stat-item">
            <span className="stat-value">54</span>
            <span className="stat-label">Cards Completed</span>
          </div>
        </div>

        <div className="completion-actions">
          <button
            className="action-button primary"
            onClick={onNewSession}
          >
            New Session
            <span className="button-subtitle">Same exercises</span>
          </button>

          <button
            className="action-button secondary"
            onClick={onCloseApp}
          >
            Close App
            <span className="button-subtitle">Randomize on next open</span>
          </button>
        </div>

        <div className="completion-note">
          <p>
            <strong>New Session:</strong> Start fresh with the same exercise assignments
          </p>
          <p>
            <strong>Close App:</strong> When you reopen, all exercises will be randomly reassigned
          </p>
        </div>
      </div>
    </div>
  );
};

export default CompletionScreen;
