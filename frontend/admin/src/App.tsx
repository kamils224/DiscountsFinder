import React from 'react';
import { Routes, Route } from "react-router-dom";
import './App.css';
import TasksList from "./views/tasks-list";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<TasksList/>}/>
      </Routes>
    </div>
  );
}

export default App;
