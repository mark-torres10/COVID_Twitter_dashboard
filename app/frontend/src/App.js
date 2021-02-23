import React from 'react'; 
import Sidebar from "./Sidebar"; 
import Header from "./Header"; 
import TrendingCOVIDTweets from "./TrendingCOVIDTweets"; 
import CurrentCOVIDNews from "./CurrentCOVIDNews"; 
import CurrentCOVIDCounts from "./CurrentCOVIDCounts"; 

import './static/App.css'; 

const App = () => {
  return (
    <div className="app-div">
      <div className="app-flex-div">
        {/* Sidebar */}
        <Sidebar className="sidebar-div"/>
        {/* Header + Dashboard */}
        <div className="header-dash-flex-div">
          <Header className="header-div"/>
          <div className="dashboard-div">
            <TrendingCOVIDTweets className="trending-covid-tweets"/>
            <CurrentCOVIDNews />
            <CurrentCOVIDCounts />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App