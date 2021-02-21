import React from 'react'; 
import Sidebar from "./Sidebar"; 
import Header from "./Header"; 
import './static/App.css'; 

const App = () => {
  return (
    <div className="app-div">
      <div className="app-flex-div">
        {/* Sidebar */}
        {/*
        <div className="sidebar-div">Sidebar Div</div>
        */}
        <Sidebar/>
        {/* Header + Dashboard */}
        <div className="header-dash-flex-div">
          <Header className="header-div"/>
          {/*
          <div className="header-div">Header Div</div>
          */}
          <div className="dashboard-div">Dashboard div</div>
        </div>
      </div>
    </div>
  )
}

export default App