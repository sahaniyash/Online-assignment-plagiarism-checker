import React from 'react';
import './App.css';

function Landing() {
  return (
    <div className="app">
      <header className="header">
        <h1>Plagiarism Checker</h1>
      </header>
      <main className="main-content">
        <div className="plagiarism-check-form">
          {/* Your plagiarism checking form can go here */}
          {/* You can add file upload fields and a button to check plagiarism */}
        </div>
        <div className="plagiarism-results">
          {/* Display plagiarism results here */}
          {/* You can show the percentages and other information here */}
        </div>
      </main>
      <footer className="footer">
        &copy; 2023 Plagiaracheck Website
      </footer>
    </div>
  );
}

export default Landing;
