import React, { useState } from 'react';
import Chat from './Chat';


export default function QA({onSwitchPage, currentRepo}) {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleQuestionInput = (event) => {
        setQuestion(event.target.value);
    };

    const handleQuestion = (event) => {

        // URL of the API endpoint
        const apiUrl = '/repos/'+currentRepo

        // Data to send in the request
        const requestData = {
        question: question
        };

        const headers = new Headers();
        headers.append('Content-Type', 'application/json');

        const requestOptions = {
        method: 'PUT',
        headers: headers,
        body: JSON.stringify(requestData) // Convert data to JSON string
        };

        // Make the POST request using fetch()
        fetch(apiUrl, requestOptions).then(response => response.json()).then(data => {
            setAnswer(data['answer']);
        }).catch(error => {
            console.error('Error:', error);
        });

    };

    return (
        <div>
            <div>
                <div className="inline-block-child">
                <p>Current Repo: {currentRepo}</p>
                </div>
                <div className="inline-block-child">
                <button onClick={onSwitchPage}>Switch Repo</button>
                </div>
            </div>
            <div>
                <Chat currentRepo={currentRepo}/>
            </div>
            {/* <div class="qa-item">
                <input
                    type="text"
                    value={question}
                    onChange={handleQuestionInput}
                    placeholder="Enter question here"
                    />
                <button onClick={handleQuestion}>Submit</button>
                <p>Answer: {answer}</p>
            </div> */}
        </div>
    );
};
