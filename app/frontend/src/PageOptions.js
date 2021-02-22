import React from 'react'; 
import "./static/PageOptions.css"; 

const PageOptions = () => {
    return (
        <div className="page-options">
            <a className="option" href="./">Summary</a>
            <a className="option" href="./">Map</a>
            <a className="option" href="./">Visualizations</a>
        </div>
    ); 
}

export default PageOptions; 