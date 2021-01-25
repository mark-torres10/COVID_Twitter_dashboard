import React from 'react'; 
import './static/Dashboard.css'; 
import DashboardSummaryStats from './DashboardSummaryStats'; 
import DashboardMap from './DashboardMap'; 
import DashboardCounts from './DashboardCounts'; 
import DashboardTimeSeries from './DashboardTimeSeries'; 

const Dashboard = () => {
    return (
        <div className="dashboard">
            {/* Header for summary statas*/}
            <div className="dashboard-summary-stats">
                <DashboardSummaryStats />
            </div>
            {/* Main graphs for dashboard*/}
            <div className="dashboard-main">
                <div className="dashboard-main-map-counts">
                    <DashboardMap />
                    <DashboardCounts />
                </div>
                <div className="dashboard-main-timeSeries">
                    <DashboardTimeSeries />
                </div>
            </div>
        </div>
    )
}

export default Dashboard; 