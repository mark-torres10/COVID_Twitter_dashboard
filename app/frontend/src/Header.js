import React from 'react'; 
import PageOptions from "./PageOptions"; 

import './static/Header.css'; 

const Header = () => {
    return(
        <div className="header-div">
            <p>This is a header</p>
            <p>Here is more header text</p>
            <PageOptions className="page-options"/>
        </div>
    )
}

export default Header; 