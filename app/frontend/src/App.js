import React from 'react'; 
import Sidebar from "./Sidebar"; 
import Header from "./Header"; 
import PageOptions from "./PageOptions"; 
import './static/App.css'; 

const App = () => {
  return (
    <div className="app-div">
      <div className="app-flex-div">
        {/* Sidebar */}
        {/*
        <div className="sidebar-div">Sidebar Div</div>
        */}
        <Sidebar className="sidebar-div"/>
        {/* Header + Dashboard */}
        <div className="header-dash-flex-div">
          <Header className="header-div"/>
          <div className="dashboard-div">
            Dashboard div
            <div className="covid-trending-tweets-div">This is the trending COVID tweets </div>
            <div className="covid-current-news-div">This is what's being said about COVID right now</div>
            <div className="covid-counts-div">This is the current COVID counts (cases, deaths, vaccinations)</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App