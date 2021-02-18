import React from 'react'; 
import './static/DashboardCounts.css'; 
import counts from './assets/placeholders/counts.png'; 

const DashboardCounts = () => {
    return (
        <div className="dashboard-counts">
            <img className="counts" src={counts} alt="Placeholder count data"/>
        </div>
    )
}

export default DashboardCounts; 