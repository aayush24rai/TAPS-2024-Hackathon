// OverlayImage.js
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; // Import useNavigate
import './OverlayImage.css'; // Ensure this path is correct based on your project structure
import map from './images/map.jpg'; // Import your image file correctly

const OverlayImage = () => {
  const navigate = useNavigate(); // Initialize useNavigate
  const location = useLocation();
  const email = location.state.email;

  const numbers = [
    24, 13, 1, 2, 34, 35, 23, 17, 26, 28, 30, 24, 19, 15, 8, 5,
    7, 12, 10, 11, 21, 11, 20, 26, 4, 30, 5, 25, 33, 27, 9, 27,
    12, 16, 17, 15, 6, 16, 28, 3, 1, 29, 22, 29, 2, 23, 31,
    19, 25, 18, 7, 8, 18, 4, 14, 35, 33, 13, 21, 10, 31, 32,
    34, 22, 14, 6, 20, 3, 9, 33, 32, 9, 30, 28, 27, 14, 22,
    23, 13, 24, 22, 1, 29, 18, 18, 4, 29, 9, 16, 25, 21, 33,
    16, 31, 3, 7, 7, 34, 15, 32, 6, 11, 11, 6, 31, 24, 12,
    20, 8, 2, 23, 10, 26, 17, 3, 19, 17, 34, 5, 8, 32, 12,
    25, 15, 13, 28, 5, 20, 10, 4, 19, 21, 1, 26, 14, 27, 2, 30
  ];

  const handleButtonClick = (number) => {
    console.log(`Button ${number} clicked`);
    // Navigate to the button page (replace '/button-page' with your actual route)
    navigate(`/button/${number}`); // Adjust the path as necessary
  };

  return (
    <div className="main-container">
      <h1 className="title">Plot Heat Map</h1>
      <div className="image-container">
        {/* Use the imported map variable here */}
        <img src={map} alt="Overlay" className="overlay-image" />
        <div className="button-grid">
          {numbers.map((number, index) => (
            <button 
              key={index} 
              className="grid-button" 
              onClick={() => handleButtonClick(number)}
            >
              <div className="number-box">{number}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OverlayImage;
