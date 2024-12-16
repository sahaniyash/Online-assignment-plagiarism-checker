import React from 'react';
import './App.css';
import PlagiarismChecker from './components/displayResult';

function App() {
  return (
    <div className="app">
      <header className="header">
      </header>
      <main className="main-content">
        <div className="plagiarism-check-form">
          <PlagiarismChecker />
        </div>
        <div className="plagiarism-results">
          {/* Display plagiarism results here */}
          {/* You can show the percentages and other information here */}
        </div>
      </main>
      <footer className="footer">
        &copy; 2023 PlagiaCheck Website
      </footer>
    </div>
  );
}

export default App;
