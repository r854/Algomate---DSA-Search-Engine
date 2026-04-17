const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

// --- Middleware ---
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// --- Routes ---

// Landing page — show search page directly
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'data.html'));
});

// Serve problems data for client-side search
app.get('/problems-data.json', (req, res) => {
  res.sendFile(path.join(__dirname, 'filtering', 'FreeLeetcode.json'));
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
