import React from 'react'; 
import "./static/COVIDTweet.css"; 
import exampleTweet from "./assets/placeholders/sample_musk_tweet.jpg"; 

const COVIDTweet = () => {
    return (
        <div className="covid-tweet-container">
            {/* Figure to hold COVID tweet */}
            <div className="covid-tweet-img">
                <img src={exampleTweet} alt="tweet" height="73"/>
            </div>
            <div className="covid-tweet-description">Description</div>
        </div>
    )
}

export default COVIDTweet; 