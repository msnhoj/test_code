// LocalStorage keys
const STORAGE_KEYS = {
  SESSION: 'pt_deck_session',
  SUIT_ASSIGNMENTS: 'pt_deck_suit_assignments',
  JOKER_EXERCISE: 'pt_deck_joker_exercise',
};

// Check if localStorage is available
export const isStorageAvailable = () => {
  try {
    const test = '__storage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
};

// Save session state
export const saveSession = (currentCardIndex, deck) => {
  if (!isStorageAvailable()) return false;

  try {
    const sessionData = {
      currentCardIndex,
      deck,
      timestamp: Date.now(),
    };
    localStorage.setItem(STORAGE_KEYS.SESSION, JSON.stringify(sessionData));
    return true;
  } catch (e) {
    console.error('Failed to save session:', e);
    return false;
  }
};

// Load session state
export const loadSession = () => {
  if (!isStorageAvailable()) return null;

  try {
    const data = localStorage.getItem(STORAGE_KEYS.SESSION);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    console.error('Failed to load session:', e);
    return null;
  }
};

// Clear session data
export const clearSession = () => {
  if (!isStorageAvailable()) return false;

  try {
    localStorage.removeItem(STORAGE_KEYS.SESSION);
    return true;
  } catch (e) {
    console.error('Failed to clear session:', e);
    return false;
  }
};

// Save suit assignments (persists across app closes)
export const saveSuitAssignments = (assignments) => {
  if (!isStorageAvailable()) return false;

  try {
    localStorage.setItem(STORAGE_KEYS.SUIT_ASSIGNMENTS, JSON.stringify(assignments));
    return true;
  } catch (e) {
    console.error('Failed to save suit assignments:', e);
    return false;
  }
};

// Load suit assignments
export const loadSuitAssignments = () => {
  if (!isStorageAvailable()) return null;

  try {
    const data = localStorage.getItem(STORAGE_KEYS.SUIT_ASSIGNMENTS);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    console.error('Failed to load suit assignments:', e);
    return null;
  }
};

// Clear suit assignments (triggers new randomization)
export const clearSuitAssignments = () => {
  if (!isStorageAvailable()) return false;

  try {
    localStorage.removeItem(STORAGE_KEYS.SUIT_ASSIGNMENTS);
    localStorage.removeItem(STORAGE_KEYS.JOKER_EXERCISE);
    return true;
  } catch (e) {
    console.error('Failed to clear suit assignments:', e);
    return false;
  }
};

// Save joker exercise
export const saveJokerExercise = (exercise) => {
  if (!isStorageAvailable()) return false;

  try {
    localStorage.setItem(STORAGE_KEYS.JOKER_EXERCISE, JSON.stringify(exercise));
    return true;
  } catch (e) {
    console.error('Failed to save joker exercise:', e);
    return false;
  }
};

// Load joker exercise
export const loadJokerExercise = () => {
  if (!isStorageAvailable()) return null;

  try {
    const data = localStorage.getItem(STORAGE_KEYS.JOKER_EXERCISE);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    console.error('Failed to load joker exercise:', e);
    return null;
  }
};

// Clear all app data
export const clearAllData = () => {
  if (!isStorageAvailable()) return false;

  try {
    Object.values(STORAGE_KEYS).forEach(key => {
      localStorage.removeItem(key);
    });
    return true;
  } catch (e) {
    console.error('Failed to clear all data:', e);
    return false;
  }
};
