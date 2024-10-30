import React, { PureComponent } from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useLocation } from 'react-router-dom';
import './ButtonPage.css';

const ButtonPage = () => {
  const { id } = useParams();  // Get the button ID from the URL
  const location = useLocation();
  const email = location.state.email;
  const [weatherData, setWeatherData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedWeek, setSelectedWeek] = useState("Current");
  const agriculturePhrases = [
    "Because every drop counts (we actually counted them) 📊",
    "Optimizing your agriculture, one drop at a time! 💧",
    "Because your crops deserve better than guesswork 🌱",
    "Turning water waste into water wisdom 🚰",
    "Taking the 'irritating' out of irrigation 😉",
    "Helping Mother Nature work smarter 🌍",
  ];
  const typingSpeed = 150;
  const deletingSpeed = 100;
  const pauseBetweenWords = 75;
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  
  useEffect(() => {
    if (isLoading) {
      const currentWord = agriculturePhrases[currentWordIndex];
      const isEndOfWord = displayedText === currentWord;
      const isStartOfWord = displayedText === '';
  
      let timeout;
  
      if (isEndOfWord && !isDeleting) {
        timeout = setTimeout(() => setIsDeleting(true), pauseBetweenWords);
      } else if (isDeleting && isStartOfWord) {
        setIsDeleting(false);
        setCurrentWordIndex((prevIndex) => (prevIndex + 1) % agriculturePhrases.length);
      } else {
        timeout = setTimeout(() => {
          setDisplayedText((prevText) =>
            isDeleting
              ? prevText.slice(0, -1)
              : currentWord.slice(0, prevText.length + 1)
          );
        }, isDeleting ? deletingSpeed : typingSpeed);
      }
  
      return () => clearTimeout(timeout);
    }
  }, [displayedText, isDeleting, currentWordIndex, agriculturePhrases]);

  useEffect(() => {
    if (!weatherData) {
      setWeatherData({});
      console.log("email", email);
      console.log("famr_id", id);
      const fd = new FormData();
      fd.append("farm_id", id);
      fd.append("email", email)
      axios.post("http://127.0.0.1:5000/get/plot/info", fd, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      })
      .then(response => handleResponse(response.data))
      .catch(error => console.log(error));
    }
  }, [id]);

  const handleResponse = (data) => {
    console.log("DATA: ", data);
    setIsLoading(false);
    if (!weatherData && data.status == "200") {
      setWeatherData(data);
    }
  }

  const calculateOptimalIrrigationPercentage = () => {
    if (weatherData.given_irrigation == 0) {
      return 0;
    }
    const saved = ((weatherData.given_irrigation - weatherData.optimal_irrigation) / weatherData.optimal_irrigation) * 100;
    return Math.round(saved * 100) / 100;
  }

  const calculateOptimizedPercentSavings = () => {
      const costGiven = weatherData.money_info.plot_cost_given;
      const costOptimized = weatherData.money_info.plot_cost_optimized;

      if (costGiven == 0) {
          return 0;
      }
      const saved = costGiven - costOptimized;
      return Math.round(saved * 100) / 100;
  }


  const calculateGallonsSaved = () => {
      if (weatherData.money_info.plot_irrigation_optimized_gallons == 0) {
        return 0;
      }
      const gallons = weatherData.money_info.plot_irrigation_given_gallons - weatherData.money_info.plot_irrigation_optimized_gallons;
      return Math.round(gallons * 100) / 100;
  }

  if (isLoading) {
    return (
      <div className='loading-container'>
        <h1 className='loading-phrase'>{displayedText}</h1>
        <div className="loader">
            <span></span>
        </div>
      </div>
    )
  }
  return (
    <div className='optimize-container'>
      <div className='data-container'>
        <div className='header'>
          <h1 className='h'>Week: {selectedWeek}</h1>
        </div>
        <div className='pop-divs'>
          <div className='popup'>
            <h3 className='pop-h3'>Optimized Irrigation</h3>
            <h1 className='pop-h'>{weatherData.optimal_irrigation}mm</h1>
            <h1 className='pop-h'>{calculateOptimalIrrigationPercentage()}% optimization</h1>
          </div>
          <div className='popup'>
            <h3 className='pop-h3'>Cost</h3>
            <h1 className='pop-h'>${Math.round(weatherData.money_info.plot_cost_optimized * 100) / 100}/plot</h1>
            <h1 className='pop-h'>${calculateOptimizedPercentSavings()} saved</h1>
          </div>
          <div className='popup'>
            <h3 className='pop-h3'>Energy</h3>
            <h1 className='pop-h'>{weatherData.energy_info.plot_optimized_energy} kw/h saved</h1>
            <h1 className='pop-h'>{calculateGallonsSaved()} gallons saved</h1>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ButtonPage;
