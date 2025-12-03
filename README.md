# Military PT Deck Workout PWA

A production-ready Progressive Web App (PWA) for military-themed physical training using the "deck of cards" workout method.

## 🎯 Features

- **Randomized Exercises**: Each suit is randomly assigned to a PT exercise when the app opens
- **54-Card Workout**: Full deck (52 cards + 2 Jokers) with exercise-rep combinations
- **Progressive Tracking**: Visual progress bar showing cards completed
- **Session Persistence**: Resume your workout if the app refreshes mid-session
- **Offline Capability**: Full functionality without internet connection
- **Mobile-First Design**: Optimized for touch interactions and mobile devices
- **Military Aesthetic**: Dark theme with tactical colors and military styling

## 🏋️ How It Works

### Card Values
- **Ace**: 1 rep
- **2-9**: Face value (2-9 reps)
- **10/J/Q/K**: 10 reps
- **Joker**: 15 reps (random exercise)

### Exercise Assignments
Each time you close and reopen the app:
- The 4 suits are randomly assigned to different exercises
- Jokers get a random exercise (different from suit assignments)
- Assignments persist while the app stays open

### Workout Flow
1. Open the app (exercises are randomized)
2. Draw a card
3. Complete the exercise for the specified reps
4. Tap the card to advance
5. Continue through all 54 cards
6. Choose to start a new session or close the app

## 🚀 Quick Start

### Prerequisites
- Node.js 14+ and npm

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd military-pt-deck

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

### Build for Production

```bash
# Create optimized production build
npm run build

# The build folder is ready to deploy
```

## 📦 Deployment

### Deploy to GitHub Pages

1. Add homepage to `package.json`:
```json
"homepage": "https://yourusername.github.io/military-pt-deck"
```

2. Install gh-pages:
```bash
npm install --save-dev gh-pages
```

3. Add deploy scripts to `package.json`:
```json
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}
```

4. Deploy:
```bash
npm run deploy
```

### Deploy to Netlify

1. Build the project:
```bash
npm run build
```

2. Drag and drop the `build` folder to Netlify
   OR
   Connect your GitHub repo and set:
   - Build command: `npm run build`
   - Publish directory: `build`

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Heroku

Create a `server.js` file:
```javascript
const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'build')));

app.get('/*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT);
```

Add to `package.json`:
```json
"scripts": {
  "start": "node server.js",
  "heroku-postbuild": "npm run build"
}
```

Deploy:
```bash
heroku create
git push heroku main
```

## 🎨 Customization

### Adding New Exercises

Edit `src/utils/exercises.js`:

```javascript
export const EXERCISES = [
  { id: 'new-exercise', name: 'New Exercise', type: 'reps' },
  // ... other exercises
];
```

Exercise types:
- `'reps'`: Count-based exercises
- `'seconds'`: Time-based exercises (e.g., Plank Hold)

### Changing Colors

Edit CSS files in `src/styles/` and `src/components/`:
- Primary color (green): `#27ae60`
- Background: `#0d0d0d`, `#1a1a1a`
- Accent colors: Olive/Grey tactical tones

### Modifying Card Values

Edit `src/utils/exercises.js` to change the `RANKS` object:

```javascript
export const RANKS = {
  ACE: { display: 'A', value: 1 },
  // Modify values as needed
};
```

## 📱 PWA Installation

### iOS (Safari)
1. Open the app in Safari
2. Tap the Share button
3. Scroll and tap "Add to Home Screen"
4. Tap "Add"

### Android (Chrome)
1. Open the app in Chrome
2. Tap the menu (three dots)
3. Tap "Add to Home Screen" or "Install App"
4. Confirm installation

### Desktop (Chrome/Edge)
1. Open the app
2. Look for the install icon in the address bar
3. Click "Install"

## 🔧 Technical Architecture

### Project Structure
```
military-pt-deck/
├── public/
│   ├── index.html          # HTML template
│   ├── manifest.json       # PWA manifest
│   ├── service-worker.js   # Service worker for offline
│   └── robots.txt
├── src/
│   ├── components/         # React components
│   │   ├── Card.js
│   │   ├── ProgressBar.js
│   │   └── CompletionScreen.js
│   ├── utils/              # Utilities
│   │   ├── exercises.js    # Exercise data & deck logic
│   │   └── storage.js      # localStorage management
│   ├── styles/             # Global styles
│   │   └── App.css
│   ├── App.js              # Main app component
│   ├── index.js            # Entry point
│   └── serviceWorkerRegistration.js
└── package.json
```

### State Management
- React hooks (`useState`, `useEffect`, `useCallback`)
- localStorage for persistence
- Session state restoration on page refresh

### Storage Keys
- `pt_deck_session`: Current workout session
- `pt_deck_suit_assignments`: Exercise-to-suit mappings
- `pt_deck_joker_exercise`: Joker exercise assignment

### Key Components

**App.js**: Main application logic, state management, session handling

**Card.js**: Displays current card with exercise, suit, and rep count

**ProgressBar.js**: Visual progress indicator

**CompletionScreen.js**: End-of-workout screen with options

## 🧪 Testing

### Manual Testing Checklist

- [ ] App loads without errors
- [ ] Exercises randomize on first load
- [ ] Cards advance on tap/click
- [ ] Progress bar updates correctly
- [ ] Session persists on page refresh
- [ ] Completion screen appears after last card
- [ ] "New Session" keeps same exercises
- [ ] "Close App" clears session
- [ ] "Full Reset" generates new assignments
- [ ] App works offline
- [ ] PWA can be installed
- [ ] Touch interactions feel responsive
- [ ] Responsive design works on all screen sizes

### Browser Testing

Test on:
- Chrome/Edge (desktop & mobile)
- Safari (iOS)
- Firefox
- Samsung Internet (Android)

## 🎯 Before Production Deployment

### Required: Generate PWA Icons

The app needs proper icons before public deployment:

1. Create a 512x512 PNG logo with military theme
2. Use [RealFaviconGenerator](https://realfavicongenerator.net/) or [PWA Builder](https://www.pwabuilder.com/imageGenerator)
3. Replace placeholder files:
   - `public/favicon.ico`
   - `public/logo192.png`
   - `public/logo512.png`

### Optional Enhancements

- Add Google Analytics
- Implement exercise tutorials/descriptions
- Add workout history/statistics
- Include timer for timed exercises
- Add sound effects/haptic feedback
- Social sharing features
- Custom workout presets

## 🐛 Troubleshooting

### App won't install as PWA
- Ensure HTTPS (required for PWA)
- Check service worker registration in DevTools
- Verify manifest.json has valid icons

### Session not persisting
- Check browser's localStorage is enabled
- Clear localStorage and try again: `localStorage.clear()`

### Build fails
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node.js version (14+ required)

### Service worker not updating
- Hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)
- Unregister service worker in DevTools
- Clear browser cache

## 📄 License

MIT License - feel free to use for personal or commercial projects

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 💪 Exercise Pool

The app includes these military PT exercises:
- Push-ups
- Sit-ups
- Squats
- Burpees
- Mountain Climbers
- Flutter Kicks
- Jumping Jacks
- Lunges
- Plank Hold (seconds)
- Air Squats
- Diamond Push-ups
- Wide Push-ups

## 🎖️ Workout Tips

1. **Warm up** before starting (5-10 minutes)
2. **Pace yourself** - it's 54 cards worth of exercises
3. **Take breaks** as needed between cards
4. **Focus on form** over speed
5. **Stay hydrated** throughout
6. **Cool down** and stretch after completion

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check the troubleshooting section
- Review the technical documentation above

---

Built with ⚡ React & 💪 Military PT Standards
