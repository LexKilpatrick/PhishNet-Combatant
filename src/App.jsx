import React from 'react';
import './index.css'; // Importing the CSS file
import { useState, useEffect } from 'react';

function App() {
  const showMessage = () => {
    var spawn = require("child_process").spawn;
    console.log("Hey")
    spawn("powershell.exe",[".\script.ps1"]);
  };
  const [isAnimated, setIsAnimated] = useState(false);


  const handleScrollAnimation = () => {
    const triggerHeight = 200; // The scroll position (in pixels) to trigger the animation
    if (window.scrollY > triggerHeight) {
      setIsAnimated(true);
    } else {
      setIsAnimated(false);
    }
  };

  // useEffect hook to add and remove the scroll event listener
  useEffect(() => {
    window.addEventListener('scroll', handleScrollAnimation);

    // Cleanup function to remove the event listener
    return () => window.removeEventListener('scroll', handleScrollAnimation);
  }, []);

  return (
    <div>
      <div className="flex-container">
        <img src="./fishlogo.png" alt="Descriptive Text" className="PhishNet" />
        <div class="gradient-text"><h1 class="name">PHISHNET</h1></div>
      </div>
      <img src="./scamphoto.png" alt="Image Description" className="scamphoto" />
      <h1 className="mission">PhishNet is an online web application, designed to help users identify Phising attempts</h1>
      <br />
      <div className={isAnimated ? "animate" : ""}>
      {/* Large textarea for lengthy email input */}
      <div className="input-container">
      <div className="row">
            <div className="row-content">
              {/* Row 1 Content */}
              <br /><br />
              <img src="./Machine.jpg" alt="Image Description" className="image-between-lines" />
              <h1 class="subsections">Machine Learning Classification Model<p className="content-paragraph">To create PhishNet’s custom AI model we deploy transfer learning by fine-tuning DistillBERT, an older (2019) smaller (250 million parameter) model which was created to make improvements on the previously existing BERT model. The dataset we used consisted of 18,600 emails, 39% of which were phishing emails. The model was trained in Google’s Colab on a T4 GPU and it took 1 hour. We rely heavily on a notebook released by DIMA806 on Kaggle, a senior data scientist in Denmark. The Colab can be found on our repository, and at the top DIMA806 is cited. </p></h1>
            </div>
          </div>
          <br /><br />
          <div className="row">
            <div className="row-content">
              {/* Row 2 Content */}
              <img src="./linkanalysis.png" alt="Image Description" className="image-between-lines" />
              <h1 class="subsections">Link Analysis<p className="content-paragraph">To find links in each forwarded email we deploy RegEx, along with the library URLExtract. Once links are extracted, we process them with ipqualityscore’s API for determining link legitimacy. It returns JSON describing many different attributes per each link, which we cut down and organize in a digestible format. </p></h1>
            </div>
          </div>
          <br /><br />
          <div className="row">
            <div className="row-content">
              {/* Row 3 Content */}
              <img src="./emailanalysis.jpg" alt="Image Description" className="image-between-lines" />
              <h1 class="subsections">Email Domain Analysis<p className="content-paragraph">In order to process domains, we run a function which identifies suspicious emails on the basis of domain lengths and abnormal characters. We then deploy ipqualityscore’s API to further determine if the email is disposable and if it was found in recent leaks. 
</p></h1>
            </div>
          </div>
          <br /><br /><br /><br /><br />
        <h3 class="email1">Email Phising Analysis</h3>
        <p class="email2">Powered by our self-trained machine learning model</p>
        <textarea placeholder="Type your email here..."></textarea>
      </div>
      <button onClick={showMessage}>Process</button>
      </div>
    </div>
  );
}

export default App;