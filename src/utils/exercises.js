// Military PT Exercise Pool
export const EXERCISES = [
  { id: 'pushups', name: 'Push-ups', type: 'reps' },
  { id: 'situps', name: 'Sit-ups', type: 'reps' },
  { id: 'squats', name: 'Squats', type: 'reps' },
  { id: 'burpees', name: 'Burpees', type: 'reps' },
  { id: 'mountain-climbers', name: 'Mountain Climbers', type: 'reps' },
  { id: 'flutter-kicks', name: 'Flutter Kicks', type: 'reps' },
  { id: 'jumping-jacks', name: 'Jumping Jacks', type: 'reps' },
  { id: 'lunges', name: 'Lunges', type: 'reps' },
  { id: 'plank', name: 'Plank Hold', type: 'seconds' },
  { id: 'air-squats', name: 'Air Squats', type: 'reps' },
  { id: 'diamond-pushups', name: 'Diamond Push-ups', type: 'reps' },
  { id: 'wide-pushups', name: 'Wide Push-ups', type: 'reps' },
];

// Suits in a standard deck
export const SUITS = {
  HEARTS: { symbol: '♥', name: 'Hearts', color: 'red' },
  DIAMONDS: { symbol: '♦', name: 'Diamonds', color: 'red' },
  CLUBS: { symbol: '♣', name: 'Clubs', color: 'black' },
  SPADES: { symbol: '♠', name: 'Spades', color: 'black' },
};

// Card ranks
export const RANKS = {
  ACE: { display: 'A', value: 1 },
  TWO: { display: '2', value: 2 },
  THREE: { display: '3', value: 3 },
  FOUR: { display: '4', value: 4 },
  FIVE: { display: '5', value: 5 },
  SIX: { display: '6', value: 6 },
  SEVEN: { display: '7', value: 7 },
  EIGHT: { display: '8', value: 8 },
  NINE: { display: '9', value: 9 },
  TEN: { display: '10', value: 10 },
  JACK: { display: 'J', value: 10 },
  QUEEN: { display: 'Q', value: 10 },
  KING: { display: 'K', value: 10 },
};

// Shuffle array using Fisher-Yates algorithm
export const shuffleArray = (array) => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

// Randomly assign exercises to suits
export const assignExercisesToSuits = () => {
  const shuffledExercises = shuffleArray(EXERCISES);
  const suitKeys = Object.keys(SUITS);

  const assignments = {};
  suitKeys.forEach((suit, index) => {
    assignments[suit] = shuffledExercises[index];
  });

  return assignments;
};

// Get a random exercise for jokers (excluding suit assignments)
export const getRandomJokerExercise = (suitAssignments) => {
  const assignedExerciseIds = Object.values(suitAssignments).map(ex => ex.id);
  const availableExercises = EXERCISES.filter(
    ex => !assignedExerciseIds.includes(ex.id)
  );

  if (availableExercises.length === 0) {
    // Fallback to any random exercise if all are assigned
    return EXERCISES[Math.floor(Math.random() * EXERCISES.length)];
  }

  return availableExercises[Math.floor(Math.random() * availableExercises.length)];
};

// Generate a complete deck of 54 cards
export const generateDeck = (suitAssignments, jokerExercise) => {
  const deck = [];

  // Generate 52 standard cards (4 suits x 13 ranks)
  Object.keys(SUITS).forEach(suitKey => {
    Object.keys(RANKS).forEach(rankKey => {
      deck.push({
        id: `${rankKey}_${suitKey}`,
        suit: suitKey,
        rank: rankKey,
        exercise: suitAssignments[suitKey],
        reps: RANKS[rankKey].value,
        isJoker: false,
      });
    });
  });

  // Add 2 Jokers
  deck.push({
    id: 'JOKER_1',
    suit: null,
    rank: null,
    exercise: jokerExercise,
    reps: 15,
    isJoker: true,
  });

  deck.push({
    id: 'JOKER_2',
    suit: null,
    rank: null,
    exercise: jokerExercise,
    reps: 15,
    isJoker: true,
  });

  return shuffleArray(deck);
};
