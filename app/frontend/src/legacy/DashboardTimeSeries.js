import React from 'react'; 
import './static/DashboardTimeSeries.css'; 
import timeSeries from './assets/placeholders/covid19_timeSeries.jpeg'; 

const DashboardTimeSeries = () => {
    return (
        <div className="dashboard-time-series">
            {/* Placeholder time series */}
            <img className="time-series" src={timeSeries} alt="COVID19 Time Series"/>
        </div>
    )
}

export default DashboardTimeSeries; 