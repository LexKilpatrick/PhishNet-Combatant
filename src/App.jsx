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

      
      {/* Large textarea for lengthy email input */}
      <div className="input-container">
        <textarea placeholder="Type your email here..."></textarea>
      </div>
      <button onClick={showMessage}>Process</button>
    </div>
  );
}

export default App;