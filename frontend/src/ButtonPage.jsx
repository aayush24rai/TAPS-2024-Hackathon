import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ButtonPage = () => {
  const { id } = useParams();  // Get the button ID from the URL
  console.log(id);

  useEffect(() => {
      const fd = new FormData();
      fd.append("farm_id", id);
      axios.post("http://127.0.0.1:5000/get/plot/info", fd, {
          headers: {
              'Content-Type': 'multipart/form-data',
          }
      })
      .then(response => console.log(response))
      .catch(error => console.log(error))
  }, [])

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'black' }}>
      <h1 style={{ fontWeight: 'bold', fontSize: '7em' }}>You clicked on Plot {id}</h1>
    </div>
  );
};

export default ButtonPage;
