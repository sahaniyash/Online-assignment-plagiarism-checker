import React, { useState } from 'react';
import axios from 'axios';
import '../App.css';

function PlagiarismChecker() {
  const [files, setFiles] = useState([]);
  const [plagiarismResults, setPlagiarismResults] = useState([]);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  };

  const handleFileUpload = async () => {
    if (files.length === 0) return;

    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append('file', file);
      });

      const response = await axios.post('http://localhost:5000/check-plagiarism', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const results = response.data.plagiarism_results;
      setPlagiarismResults(results);
    } catch (error) {
      console.error('Error uploading and checking plagiarism:', error);
    }
  };

  return (
    <div>
      <h1>Plagiarism Checker</h1>
      <input type="file" accept=".pdf" multiple onChange={handleFileChange} />
      <button onClick={handleFileUpload} className='check'>Check Plagiarism</button>
      {plagiarismResults.length > 0 && (
        <div>
          <h2>Plagiarism Results</h2>
          {plagiarismResults.map((result, index) => (
            <div key={index}>
              <p>File: {result.file}</p>
              <h3>Plagiarism Percentages:</h3>
              {result.results.map((plagiarism, subIndex) => (
                <div key={subIndex}>
                  <p>{plagiarism.file}: {plagiarism.plagiarism * 100}%</p>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PlagiarismChecker;