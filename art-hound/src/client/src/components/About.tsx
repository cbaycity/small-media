import React from 'react';

function About() {
    return(
    <div className="container about-me-body center-body">
        <div className="p40">
            <img className="portrait" src="public/BayardPhoto.png"></img>
        </div>
        <div className="p40 about-me-text div-body">
            <p>Art Hound is a place where artists can post their art, project updates, and other work without fearing that it will be used to train a generative AI model.</p>
            <p>We fight to ensure that our user's artwork isn't trained on by generative AI models.</p>
            <ul>
                <li>We don't allow bots to create accounts on Art Hound and work to remove comprimised accounts.</li>
                <li>We limit the number of assets an account can view per minute.</li>
                <li>We provide strong account privacy settings and allow users to easily adjust their settings.</li>
            </ul>
        </div>
    </div>
    );
};

export default About;