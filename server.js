const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { spawn } = require('child_process');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

const app = express();
const PORT = 3000;

// --- Passport Config ---
// In a real app, use environment variables for these!
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || 'YOUR_GOOGLE_CLIENT_ID';
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || 'YOUR_GOOGLE_CLIENT_SECRET';

passport.use(new GoogleStrategy({
    clientID: GOOGLE_CLIENT_ID,
    clientSecret: GOOGLE_CLIENT_SECRET,
    callbackURL: process.env.BASE_URL ? `${process.env.BASE_URL}/auth/google/callback` : "http://localhost:3000/auth/google/callback"
  },
  function(accessToken, refreshToken, profile, cb) {
    // For this hackathon app, we'll just pass the profile through
    return cb(null, profile);
  }
));

passport.serializeUser((user, done) => {
  done(null, user);
});

passport.deserializeUser((user, done) => {
  done(null, user);
});

// --- Middleware ---
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
  secret: process.env.SESSION_SECRET || 'algomate_secret_session',
  resave: false,
  saveUninitialized: true
}));
app.use(passport.initialize());
app.use(passport.session());

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// --- Routes ---

// Landing page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Login — simple hardcoded check (matches old Flask behaviour)
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  if (username === 'admin' && password === 'admin') {
    res.redirect('/problems');
  } else {
    res.redirect('/');
  }
});

// --- Authentication Routes ---

// Google Auth
app.get('/auth/google',
  passport.authenticate('google', { scope: ['profile', 'email'] }));

app.get('/auth/google/callback', 
  passport.authenticate('google', { failureRedirect: '/' }),
  (req, res) => {
    // Successful authentication, redirect to search.
    res.redirect('/search');
  });

// Logout
app.get('/logout', (req, res) => {
  req.logout((err) => {
    if (err) { return next(err); }
    res.redirect('/');
  });
});

// Problems page
app.get('/problems', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'problems.html'));
});

// Search page
app.get('/search', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'data.html'));
});

// Search query endpoint — calls the Python search worker
app.post('/query', (req, res) => {
  const searchQuery = req.body.query;

  if (!searchQuery || !searchQuery.trim()) {
    return res.json({ message: 'No results found' });
  }

  // Spawn the Python search worker
  const python = spawn('python3', [
    path.join(__dirname, 'search_worker.py'),
    searchQuery
  ]);

  let output = '';
  let errorOutput = '';

  python.stdout.on('data', (data) => {
    output += data.toString();
  });

  python.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  python.on('close', (code) => {
    if (code !== 0) {
      console.error('Python search worker error:', errorOutput);
      return res.status(500).json({ message: 'Search failed', error: errorOutput });
    }
    try {
      // Find JSON in output (skip any print/log noise before it)
      const jsonStart = output.indexOf('[');
      const jsonStr = jsonStart !== -1 ? output.slice(jsonStart) : output;
      const results = JSON.parse(jsonStr.trim());
      if (results.length === 0) {
        return res.json({ message: 'No results found' });
      }
      res.json(results);
    } catch (e) {
      console.error('Failed to parse Python output:', output);
      res.status(500).json({ message: 'Failed to parse search results' });
    }
  });
});

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Algomate server running at http://localhost:${PORT}`);
});
