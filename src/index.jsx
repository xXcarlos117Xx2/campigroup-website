import React from 'react';
import ReactDOM from 'react-dom/client';

// React Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';

// Components
import { Navegation } from './js/components/navbar/Navbar';
import { GameCards } from './js/components/card/GameCards';

//data
import gameData from './js/data/database.json';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Navegation data = {gameData}/>
    <GameCards data = {gameData}/>
  </React.StrictMode>
);
