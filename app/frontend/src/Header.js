import React from 'react'; 
import PageOptions from "./PageOptions"; 

import './static/Header.css'; 

const Header = () => {
    return(
        <div className="header-div">
            <h1 className="header-title">Covid Tweets Dashboard</h1>
            <PageOptions className="page-options"/>
        </div>
    )
}

export default Header; 