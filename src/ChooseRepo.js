import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';

export default function ChooseRepo({onSwitchPage, handleChangeRepo}) {
    const [inputValue, setInputValue] = useState('');
    const [repos, setRepos] = useState([]);

    useEffect(() => {
        fetch('/repos').then(res => res.json()).then(data => {
          // console.log(data.repo_names);
          setRepos(data.repo_names);
        });
      }, []);

    const handleRepoInput = (event) => {
        setInputValue(event.target.value);
    };

    const handleButtonClick = () => {

        // URL of the API endpoint
        const apiUrl = '/newrepo'

        // Data to send in the request
        const requestData = {
        url: inputValue
        };

        const headers = new Headers();
        headers.append('Content-Type', 'application/json');

        const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestData) // Convert data to JSON string
        };

        // Make the POST request using fetch()
        fetch(apiUrl, requestOptions).then(response => response.json()).then(data => {
            console.log('Response data:', data);
        }).catch(error => {
            console.error('Error:', error);
        });

      };


    return (
        <div>
            <div>
            <p className="choose-repo-item">Submit a new repo below</p>
            <input
            type="text"
            value={inputValue}
            onChange={handleRepoInput}
            placeholder="Enter repo url here"
            />
            <button onClick={handleButtonClick}>Submit</button>
            </div>
            <div>
            <p className="choose-repo-item">Or choose from an existing repo</p>
            <ul title="Loaded Repositories:">
            {repos.map((item, index) => (
                <li key={index}
                    onClick={() => {
                    onSwitchPage();
                    handleChangeRepo(item);
                    }}>
                    {item}
                </li>
            ))}
            </ul>
            </div>
        </div>
    );
};

