import React, { useState } from 'react';


export default function Chat({currentRepo}) {
    const [messages, setMessages] = useState([]);
    const [newQuestionText, setNewQuestionText] = useState('');



    async function sendQuestion(question) {
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

       return await fetch(apiUrl, requestOptions)
       .then(response => response.json())
       .then(responseJson => {return responseJson})
    }
  
    async function handleSendQuestion() {


      if (newQuestionText.trim() === '') return;
  
      // Create a new message object with a unique ID (you may want to use a library for this).
      const questionMessage = {
        id: Date.now(),
        text: newQuestionText,
        messageType: 'Question'
      };

      setMessages((prevMessages) => [...prevMessages, questionMessage]);

      await sendQuestion(newQuestionText).then(responseJson => {
        const answerText = responseJson['answer'];
        const answerMessage = {
            id: Date.now(),
            text: answerText,
            messageType: 'Answer'
        }
        setMessages((prevMessages) => [...prevMessages, answerMessage]);
    });

  
      // Clear the input field.
      setNewQuestionText('');
    };
  
    return (
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((message) => (
            <div key={message.id} className="message">
              <strong>{message.messageType}:</strong> {message.text}
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            placeholder="Type a Question..."
            value={newQuestionText}
            onChange={(e) => setNewQuestionText(e.target.value)}
          />
          <button onClick={async () => await handleSendQuestion()}>Send</button>
        </div>
      </div>
    );
};
