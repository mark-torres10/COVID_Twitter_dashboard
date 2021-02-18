import React from 'react'; 
import './static/DashboardMap.css'; 
import usaMap from './assets/placeholders/usa_map.png'; 

const DashboardMap = () => {
    return (
        <div className = "dashboard-map">
            {/* Placeholder image, for our eventual map */}
            <img className="map" src={usaMap} alt="Map of United States"/>
        </div>
    )
}

export default DashboardMap; 