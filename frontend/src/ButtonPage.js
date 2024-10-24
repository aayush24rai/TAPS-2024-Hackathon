import React from 'react';
import { useParams } from 'react-router-dom';

const ButtonPage = () => {
  const { id } = useParams();  // Get the button ID from the URL

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'white' }}>
      <h1 style={{ fontWeight: 'bold', fontSize: '7em' }}>You clicked on Plot {id}</h1>
    </div>
  );
};

export default ButtonPage;
