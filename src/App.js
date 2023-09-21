import './App.css';
import ChooseRepo from './ChooseRepo';
import QA from './QA';
import React, { useState } from 'react';

function App() {
  const [page, setPage] = useState('chooseRepo');
  const [currentRepo, setCurrentRepo] = useState('');


  const handleChangeRepo = (newRepo) => {
    console.log("test");
    setCurrentRepo(newRepo);
  }


  return (
    <div className="App min-vh-100 d-flex justify-content-center align-items-center">
      <div className="container">
      <h1>Analyze Your Repo</h1>
          {page === "chooseRepo" && <ChooseRepo
          onSwitchPage={() => setPage('qa')}
          handleChangeRepo={setCurrentRepo}
          />}
          {page === "qa" && <QA
          onSwitchPage={() => setPage('chooseRepo')}
          currentRepo={currentRepo}/>}
          {console.log("currentRepo: "+currentRepo)}
      </div>
    </div>
  );
}

export default App;
