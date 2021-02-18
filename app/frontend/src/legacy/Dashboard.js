import React from 'react'; 
import './static/Dashboard.css'; 
import DashboardSummaryStats from './DashboardSummaryStats'; 
import DashboardMap from './DashboardMap'; 
import DashboardCounts from './DashboardCounts'; 
import DashboardTimeSeries from './DashboardTimeSeries'; 

const Dashboard = () => {
    return (
        <div className="dashboard">
            {/* Header for summary stats*/}
            <div className="dashboard-summary-stats">
                <DashboardSummaryStats />
            </div>
            {/* Main graphs for dashboard*/}
            <div className="dashboard-main-map-counts">
                <DashboardMap className="dashboard-map"/>
                <DashboardCounts className="dashboard-counts"/>
            </div>
            <br className="clr"/>
            <div className="dashboard-main-timeSeries">
                <DashboardTimeSeries />
            </div>
        </div>
    )
}

export default Dashboard; 