import React, { PureComponent } from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import { Line } from 'react-chartjs-2';
import './ButtonPage.css';
import {Home} from 'lucide-react';

const ButtonPage = () => {
  const { id } = useParams();  // Get the button ID from the URL
  const location = useLocation();
  const navigate = useNavigate();
  const email = location.state.email;
  const [weatherData, setWeatherData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedWeek, setSelectedWeek] = useState("Current");
  const agriculturePhrases = [
    "Because every drop counts (we actually counted them) 📊",
    "Optimizing your agriculture, one drop at a time! 💧",
    "Because your crops deserve better than guesswork 🌱",
  ];
  const [showIrrigationChart, setShowIrrigationChart] = useState(false);
  const [showCostChart, setShowCostChart] = useState(false);
  const [showEnergyChart, setShowEnergyChart] = useState(false);
  const [showWeatherChart, setShowWeatherChart] = useState(false);

  const typingSpeed = 150;
  const deletingSpeed = 100;
  const pauseBetweenWords = 75;
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const dates = [
    "2024-04-25", "2024-05-23", "2024-06-11", "2024-06-18", "2024-06-25", "2024-07-02", 
    "2024-07-09", "2024-07-10", "2024-07-16", "2024-07-17", "2024-07-23", "2024-07-23", 
    "2024-07-30", "2024-08-06", "2024-08-07", "2024-08-13", "2024-08-20", "2024-08-27", 
    "2024-09-03", "2024-09-10"
  ];
  
  const dateDict = dates.reduce((dict, date, index) => {
    dict[date] = index;
    return dict;
  }, {});
  
  useEffect(() => {
    if (isLoading) {
      const currentWord = agriculturePhrases[currentWordIndex];
      const isEndOfWord = displayedText == currentWord;
      const isStartOfWord = displayedText == '';
  
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
      const fd = new FormData();
      fd.append("farm_id", id);
      fd.append("email", email)
      axios.post("http://127.0.0.1:5000/future/plot/info", fd, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      })
      .then(response => handleResponse(response.data))
      .catch(error => console.log(error));
    }
  }, [id]);

  const handleResponse = (data, call=false) => {
    console.log("DATA: ", data);
    //setIsLoading(false);
    if ((!weatherData || call) && data.status == "200") {
      setIsLoading(false);
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

  const handleIrrigationChartClick = () => {
    setShowIrrigationChart(!showIrrigationChart);
    if(showCostChart){
      setShowCostChart(!showCostChart);
    }
    else if(showEnergyChart){
      setShowEnergyChart(!showEnergyChart);
    }
    else if(showWeatherChart){
      setShowWeatherChart(!showWeatherChart);
    }
  };

  const handleCostChartClick = () => {
    setShowCostChart(!showCostChart);
    if(showIrrigationChart){
      setShowIrrigationChart(!showIrrigationChart);
    }
    else if(showEnergyChart){
      setShowEnergyChart(!showEnergyChart);
    }
    else if(showWeatherChart){
      setShowWeatherChart(!showWeatherChart);
    }
  };

  const handleEnergyChartClick = () => {
    setShowEnergyChart(!showEnergyChart);
    if(showCostChart){
      setShowCostChart(!showCostChart);
    }
    else if(showIrrigationChart){
      setShowIrrigationChart(!showIrrigationChart);
    }
    else if(showWeatherChart){
      setShowWeatherChart(!showWeatherChart);
    }
  };

  const handleWeatherChartClick = () => {
    setShowWeatherChart(!showWeatherChart);
    if(showCostChart){
      setShowCostChart(!showCostChart);
    }
    else if(showEnergyChart){
      setShowEnergyChart(!showEnergyChart);
    }
    else if(showIrrigationChart){
      setShowIrrigationChart(!showIrrigationChart);
    }
  };

  const irrigationChartData = {
    labels: ['Given Irrigation', 'Optimal Irrigation'],
    datasets: [
      {
        label: 'Irrigation (inches)',
        data: [
          weatherData?.given_irrigation || 0, // Default to 0 if undefined
          weatherData?.optimal_irrigation || 0,
        ],
        backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(153, 102, 255, 0.6)'],
      },
    ],
  };

  const irrigationChartOptions = {
    responsive: true,
    scales: {
      yAxes: [{ // Change y to yAxes
        ticks: {
          beginAtZero: true, // Ensure the y-axis starts at 0
          min: 0, // Set the minimum value of y-axis to 0
          max: 1.2, // Set the maximum value of y-axis to 1.2
          callback: (value) => value.toFixed(2), // Display y-axis values with two decimals
        },
        gridLines: {
          color: "#FFFFFF",
          zeroLineColor: "#FFFFFF"
        },
      }],
    },
  };

  const costChartData = {
    labels: ['Given Cost', 'Optimal Cost'],
    datasets: [
      {
        label: 'Cost ($)',
        data: [
          weatherData?.money_info?.plot_cost_given || 0, // Default to 0 if undefined
          weatherData?.money_info?.plot_cost_optimized || 0,
        ],
        backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(153, 102, 255, 0.6)'],
      },
    ],
  };

  const costChartOptions = {
    responsive: true,
    scales: {
      yAxes: [{ // Change y to yAxes
        ticks: {
          beginAtZero: true, // Ensure the y-axis starts at 0
          min: 1500, // Set the minimum value of y-axis to 0
          max: 2200, // Set the maximum value of y-axis to 1.2
          callback: (value) => value.toFixed(2), // Display y-axis values with two decimals
        },
        gridLines: {
          color: "#FFFFFF",
          zeroLineColor: "#FFFFFF"
        },
      }],
    },
  };

  const energyChartData = {
    labels: ['Optimal Energy'],
    datasets: [
      {
        label: 'Energy (kW/h)',
        data: [
          weatherData?.energy_info?.plot_optimized_energy || 0, // Default to 0 if undefined
        ],
        backgroundColor: ['rgba(75, 192, 192, 0.6)'],
      },
    ],
  };

  const energyChartOptions = {
    responsive: true,
    scales: {
      yAxes: [{ // Change y to yAxes
        ticks: {
          beginAtZero: true, // Ensure the y-axis starts at 0
          min: 0, // Set the minimum value of y-axis to 0
          max: 3, // Set the maximum value of y-axis to 1.2
          callback: (value) => value.toFixed(2), // Display y-axis values with two decimals
        },
        gridLines: {
          color: "#FFFFFF",
          zeroLineColor: "#FFFFFF"
        },
      }],
    },
  };

  const weatherChartData = {
    labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
    datasets: [
      {
        label: 'Average Temp (F)',
        data: weatherData?.weather_data?.map(day => day.avg_temp_f) || [0, 0, 0, 0, 0, 0, 0], // Default array if weather_data is undefined
        pointStyle: 'circle',
        pointRadius: 5,
        pointHoverRadius: 10,
        fill: false,
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: "#FFFFFF", // Line color
        pointBorderColor: "#FFFFFF", // Point border color
      },
    ],
  };

  const weatherChartOptions = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: (ctx) => 'Point Style: ' + ctx.chart.data.datasets[0].pointStyle,
      }
    },
    scales: {
      yAxes: [{ // Change y to yAxes
        gridLines: {
          color: "#FFFFFF",
          zeroLineColor: "#FFFFFF"
        },
      }]
    }
  };


  const calculateGallonsSaved = () => {
      if (weatherData.money_info.plot_irrigation_optimized_gallons == 0) {
        return 0;
      }
      const gallons = weatherData.money_info.plot_irrigation_given_gallons - weatherData.money_info.plot_irrigation_optimized_gallons;
      return Math.round(gallons * 100) / 100;
  }

  const handleSelectChange = (event) => {
    const index = event.target.value;
    setSelectedIndex(index);
    console.log("Selected Date:", dates[index]); 
    console.log("Selected Index:", index); 
  };

  const optimizeWeek = () => {
    setIsLoading(true);
    const fd = new FormData();
    setSelectedWeek(dates[selectedIndex]);
    fd.append("farm_id", id);
    fd.append("email", email);
    fd.append("date", dates[selectedIndex]);
    fd.append("index", selectedIndex);
    axios.post("http://127.0.0.1:5000/get/plot/info", fd, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
    .then(response => handleResponse(response.data, true))
    .catch(error => console.log(error));
  }

  const navigateToDashboad = () => {
    navigate("/Map", {
      state: { "email": email}
    });
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
      <div className='toggle-container'>
        <div className='n'></div>
        <div className="plot-info">
          <h1 className='pop-h3'>Plot {id}</h1>
        </div>
        <div className='items'>
          <div className='change-date-div'>
            <label htmlFor="dateDropdown" className='select-date-h'>Select Date:</label>
            <div className="select-container">
              <select
                id="dateDropdown"
                value={selectedIndex}
                onChange={handleSelectChange}
                className="modern-select"
              >
                {dates.map((date, index) => (
                  <option key={index} value={index}>
                    {date}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className='optimize-btn'>
            <button className="button" onClick={optimizeWeek}>
              ✨ Optimize
            </button>
          </div>
        </div>
      </div>
      
      <div className='right-side'>
        <div className='navbar'>
          <div className="navigate" onClick={navigateToDashboad}>
            <Home size={30} className="icon" strokeWidth={2} />
            <h1 className='nav'>Dashboard</h1>
          </div>
        </div>
        
        <div className='data-container'>
          <div className='header'>
            <h1 className='h'>Week: {selectedWeek}</h1>
          </div>
          
          <div className='pop-divs'>
            <div className='popup' onClick={handleIrrigationChartClick}>
              <h3 className='pop-h3'>Optimized Irrigation</h3>
              <h1 className='pop-h'>{weatherData.optimal_irrigation} in</h1>
              <h1 className='pop-h'>{calculateOptimalIrrigationPercentage()}% optimization</h1>
            </div>
            <div className='popup' onClick={handleCostChartClick}>
              <h3 className='pop-h3'>Cost</h3>
              <h1 className='pop-h'>${Math.round(weatherData.money_info.plot_cost_optimized * 100) / 100}/plot</h1>
              <h1 className='pop-h'>${calculateOptimizedPercentSavings()} saved</h1>
            </div>
            <div className='popup' onClick={handleEnergyChartClick}>
              <h3 className='pop-h3'>Energy</h3>
              <h1 className='pop-h'>{weatherData.energy_info.plot_optimized_energy} kw/h saved</h1>
              <h1 className='pop-h'>{calculateGallonsSaved()} gallons saved</h1>
            </div>
            <div className='popup' onClick={handleWeatherChartClick}>
              <h3 className='pop-h3'>Weather</h3>
              <h3 className='pop-h'>Avg Temp: {weatherData.avg_temp} f</h3>
              <h3 className='pop-h'>Max Temp: {weatherData.max_temp} f</h3>
              <h3 className='pop-h'>Min Temp: {weatherData.min_temp} f</h3>
            </div>
          </div>

          {showIrrigationChart && (
            <div className="chart-container">
              <Bar data={irrigationChartData} options={irrigationChartOptions} />
            </div>
          )}
          {showCostChart && (
            <div className="chart-container">
              <Bar data={costChartData} options={costChartOptions} />
            </div>
          )}
          {showEnergyChart && (
            <div className="chart-container">
              <Bar data={energyChartData} options={energyChartOptions} />
            </div>
          )}
          {showWeatherChart && (
            <div className="chart-container">
              <Line data={weatherChartData} options={weatherChartOptions} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ButtonPage;
