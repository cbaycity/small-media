import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    fetch("/members")
      .then(res => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      })}, [])
    
  return (
    <div className="App">
      <div className="App-header">
        <p>Members List</p>
        {(data.length === 0) ? (<p>loading</p>) : 
        (data.map((member, index) =>(
          <li key={index}>
            {member}
          </li>
        ))
      )}
      </div>
    </div>
  );
}

export default App;
