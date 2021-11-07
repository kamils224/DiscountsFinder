import React from 'react';
import { Routes, Route } from "react-router-dom";
import './App.css';
import ProductsTasksList from "./views/products-tasks-list";
import ProductsTaskResult from "./views/products-task-result";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<ProductsTasksList/>}/>
        <Route path="/tasks" element={<ProductsTasksList/>}/>
          <Route path="tasks/:taskId" element={<ProductsTaskResult/>}/>
      </Routes>
    </div>
  );
}

export default App;
