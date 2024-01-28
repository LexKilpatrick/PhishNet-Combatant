import React from 'react';
import './index.css'; // Importing the CSS file

function App() {
  const showMessage = () => {
    alert("Hello from React!");
  };

  return (
    <div>
      <div className="flex-container">
        <img src="./fishlogo.png" alt="Descriptive Text" className="PhishNet" />
        <div class="gradient-text"><h1 class="name">P H I S H N E T</h1></div>
      </div>
      <p className="mission">PhishNet is an online web application that was designed to spread awareness.</p>
      <button onClick={showMessage}>Process</button>
      
    </div>
  );
}

export default App;