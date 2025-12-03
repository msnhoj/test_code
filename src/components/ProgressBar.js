import React from 'react';
import './ProgressBar.css';

const ProgressBar = ({ current, total }) => {
  const percentage = (current / total) * 100;
  const remaining = total - current;

  return (
    <div className="progress-bar-container">
      <div className="progress-info">
        <span className="progress-text">
          Card {current} of {total}
        </span>
        <span className="remaining-text">
          {remaining} remaining
        </span>
      </div>
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{ width: `${percentage}%` }}
        >
          <div className="progress-bar-shine"></div>
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;
