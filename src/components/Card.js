import React from 'react';
import { SUITS, RANKS } from '../utils/exercises';
import './Card.css';

const Card = ({ card, onNext }) => {
  if (!card) return null;

  const { suit, rank, exercise, reps, isJoker } = card;

  const handleClick = () => {
    onNext();
  };

  const getSuitSymbol = () => {
    if (isJoker) return '🃏';
    return SUITS[suit]?.symbol || '';
  };

  const getSuitColor = () => {
    if (isJoker) return 'joker';
    return SUITS[suit]?.color || 'black';
  };

  const getRankDisplay = () => {
    if (isJoker) return 'JOKER';
    return RANKS[rank]?.display || '';
  };

  const getRepText = () => {
    if (exercise.type === 'seconds') {
      return `${reps} ${reps === 1 ? 'second' : 'seconds'}`;
    }
    return `${reps} ${reps === 1 ? 'rep' : 'reps'}`;
  };

  return (
    <div className="card-container" onClick={handleClick}>
      <div className={`playing-card ${getSuitColor()}`}>
        {/* Top left corner */}
        <div className="card-corner top-left">
          <div className="rank">{getRankDisplay()}</div>
          <div className="suit">{getSuitSymbol()}</div>
        </div>

        {/* Center content */}
        <div className="card-center">
          <div className="exercise-name">{exercise.name}</div>
          <div className="suit-symbol-large">{getSuitSymbol()}</div>
          <div className="reps-display">{getRepText()}</div>
        </div>

        {/* Bottom right corner */}
        <div className="card-corner bottom-right">
          <div className="rank">{getRankDisplay()}</div>
          <div className="suit">{getSuitSymbol()}</div>
        </div>
      </div>

      <div className="card-instructions">
        <p>Complete the exercise, then tap to continue</p>
      </div>
    </div>
  );
};

export default Card;
