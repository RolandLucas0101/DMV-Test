// Main entry point for the DMV Practice Test Application
// This file starts the Express server and serves both the API and React frontend

const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// For production, serve the built React app
if (process.env.NODE_ENV === 'production') {
  // Serve static files from the dist/public directory
  app.use(express.static(path.join(__dirname, 'dist/public')));
  
  // API routes would go here (import from server/routes)
  // app.use('/api', require('./server/routes'));
  
  // Catch all handler: send back React's index.html file for any non-API routes
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist/public/index.html'));
  });
}

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`DMV Practice Test App running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

module.exports = app;