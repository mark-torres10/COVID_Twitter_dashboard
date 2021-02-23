import React from 'react';
import COVIDTweet from "./COVIDTweet"; 
import "./static/TrendingCOVIDTweets.css"; 

const TrendingCOVIDTweets = () => {
    return(
        <div className="trending-covid-tweets">
            <h1>How is COVID Trending on Twitter Today?</h1>
            <div className="example-covid-tweets">
                <COVIDTweet/>
                <COVIDTweet/>
                <COVIDTweet/>
            </div>
        </div>
    )
}

export default TrendingCOVIDTweets; 