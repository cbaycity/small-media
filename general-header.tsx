import React from 'react';
import './App.css';

function App() {
  const cities = ['New York', 'London', 'Paris']
  return (
    <div className="App">
      <body>
        <div>
            {cities.map((item, index) => (<li>{item}, {index}</li>))}
        </div>
        </body>
    </div>
  );
}

export default App;