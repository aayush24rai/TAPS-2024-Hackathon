import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import OverlayImage from './OverlayImage';
import ButtonPage from './ButtonPage';  // Import the button page
import Navbar from './Navbar';  // Import the Navbar
import About from './About';  // Import the About page
import Contact from './Contact';  // Import the Contact page
import Login from './Login';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />}/>
        <Route path="/Map" element={<OverlayImage />} />  {/* Home page with buttons */}
        <Route path="/button/:id" element={<ButtonPage />} />  {/* Dynamic route for each button */}
        <Route path="/about" element={<About />} />  {/* About page */}
        <Route path="/contact" element={<Contact />} />  {/* Contact page */}
      </Routes>
    </Router>
  );
};

export default App;
