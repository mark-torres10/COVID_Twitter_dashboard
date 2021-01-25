import React from 'react'
import Header from './Header'; 
import Sidebar from './Sidebar'; 
import Dashboard from './Dashboard'; 
import "./static/App.css"; 

const App = () => {
  return (
    <div>
        <Header />
        <div className="main">
            <Sidebar className="sidebar"/>
            <Dashboard className="dashboard"/>
        </div>

    </div>
  )
}

export default App