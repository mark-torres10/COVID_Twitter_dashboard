import React from 'react'; 
import COVIDNews from "./COVIDNews"; 
import './static/CurrentCOVIDNews.css'; 

const CurrentCOVIDNews = () => {
    return (
        <div className="current-covid-news">
            <h1>Today's COVID Conversations</h1>
            <div className="covid-news-list">
                <COVIDNews/>
                <COVIDNews/>
                <COVIDNews/>
            </div>
        </div>
    )
}

export default CurrentCOVIDNews; 