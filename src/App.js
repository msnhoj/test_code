import React, { useState, useEffect, useCallback } from 'react';
import Card from './components/Card';
import ProgressBar from './components/ProgressBar';
import CompletionScreen from './components/CompletionScreen';
import {
  assignExercisesToSuits,
  getRandomJokerExercise,
  generateDeck,
} from './utils/exercises';
import {
  saveSession,
  loadSession,
  clearSession,
  saveSuitAssignments,
  loadSuitAssignments,
  clearSuitAssignments,
  saveJokerExercise,
  loadJokerExercise,
  isStorageAvailable,
} from './utils/storage';
import './styles/App.css';

function App() {
  const [deck, setDeck] = useState([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [suitAssignments, setSuitAssignments] = useState(null);
  const [jokerExercise, setJokerExercise] = useState(null);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showWarning, setShowWarning] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // Initialize or restore session
  useEffect(() => {
    if (!isStorageAvailable()) {
      setShowWarning(true);
    }

    // Try to load existing session
    const savedSession = loadSession();
    const savedAssignments = loadSuitAssignments();
    const savedJokerEx = loadJokerExercise();

    if (savedSession && savedAssignments && savedJokerEx) {
      // Restore existing session
      setSuitAssignments(savedAssignments);
      setJokerExercise(savedJokerEx);
      setDeck(savedSession.deck);
      setCurrentCardIndex(savedSession.currentCardIndex);
      setIsCompleted(savedSession.currentCardIndex >= savedSession.deck.length);
    } else {
      // No session exists, check if we have assignments from a previous app open
      if (savedAssignments && savedJokerEx) {
        // Use existing assignments but create new deck
        setSuitAssignments(savedAssignments);
        setJokerExercise(savedJokerEx);
        const newDeck = generateDeck(savedAssignments, savedJokerEx);
        setDeck(newDeck);
        setCurrentCardIndex(0);
      } else {
        // Brand new session - randomize everything
        const newAssignments = assignExercisesToSuits();
        const newJokerEx = getRandomJokerExercise(newAssignments);
        const newDeck = generateDeck(newAssignments, newJokerEx);

        setSuitAssignments(newAssignments);
        setJokerExercise(newJokerEx);
        saveSuitAssignments(newAssignments);
        saveJokerExercise(newJokerEx);

        setDeck(newDeck);
        setCurrentCardIndex(0);
      }
    }

    setIsInitialized(true);
  }, []);

  // Save session whenever deck or current card changes
  useEffect(() => {
    if (isInitialized && deck.length > 0) {
      saveSession(currentCardIndex, deck);
    }
  }, [currentCardIndex, deck, isInitialized]);

  // Handle next card
  const handleNextCard = useCallback(() => {
    if (currentCardIndex < deck.length - 1) {
      setCurrentCardIndex(prev => prev + 1);
    } else {
      setIsCompleted(true);
    }
  }, [currentCardIndex, deck.length]);

  // Start new session with same exercises
  const handleNewSession = useCallback(() => {
    if (suitAssignments && jokerExercise) {
      const newDeck = generateDeck(suitAssignments, jokerExercise);
      setDeck(newDeck);
      setCurrentCardIndex(0);
      setIsCompleted(false);
      saveSession(0, newDeck);
    }
  }, [suitAssignments, jokerExercise]);

  // Close app and clear session (exercises will randomize on next open)
  const handleCloseApp = useCallback(() => {
    clearSession();
    // Note: In a real PWA, this would close the app
    // For web, we'll just show a message
    window.alert('Session cleared! Close this tab/app. When you reopen, exercises will be randomized.');
  }, []);

  // Reset everything (for testing/debugging)
  const handleFullReset = useCallback(() => {
    clearSuitAssignments();
    clearSession();

    const newAssignments = assignExercisesToSuits();
    const newJokerEx = getRandomJokerExercise(newAssignments);
    const newDeck = generateDeck(newAssignments, newJokerEx);

    setSuitAssignments(newAssignments);
    setJokerExercise(newJokerEx);
    saveSuitAssignments(newAssignments);
    saveJokerExercise(newJokerEx);

    setDeck(newDeck);
    setCurrentCardIndex(0);
    setIsCompleted(false);
  }, []);

  if (!isInitialized) {
    return (
      <div className="app loading">
        <div className="loading-spinner"></div>
        <p>Loading PT Deck...</p>
      </div>
    );
  }

  if (isCompleted) {
    return (
      <div className="app">
        <CompletionScreen
          onNewSession={handleNewSession}
          onCloseApp={handleCloseApp}
        />
      </div>
    );
  }

  const currentCard = deck[currentCardIndex];

  return (
    <div className="app">
      <header className="app-header">
        <h1>MILITARY PT DECK</h1>
        <p className="app-subtitle">Deck of Cards Workout</p>
      </header>

      {showWarning && (
        <div className="warning-banner">
          ⚠️ Storage unavailable. Progress won't be saved.
        </div>
      )}

      <ProgressBar
        current={currentCardIndex + 1}
        total={deck.length}
      />

      {currentCard && (
        <Card
          card={currentCard}
          onNext={handleNextCard}
        />
      )}

      <button
        className="reset-button"
        onClick={handleFullReset}
        title="Completely reset and randomize exercises"
      >
        Full Reset
      </button>

      <footer className="app-footer">
        <p>Tap card to advance</p>
      </footer>
    </div>
  );
}

export default App;
