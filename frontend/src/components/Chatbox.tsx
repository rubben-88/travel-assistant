import React, { useState } from 'react';
import apiService from '../services/apiService';

interface Message {
  sender: string;
  text: string;
}

const Chatbox = () => {
  const [input, setInput] = useState('');       // To hold user input
  const [messages, setMessages] = useState<Message[]>([]); // To hold the conversation history

  // Function to send the user's query to the backend
  const sendMessage = async () => {
    if (input.trim() === '') {return;}
    
    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);
    
    const responseMessage = { sender: 'bot', text: '' };

    // Send the input to the FastAPI backend
    try {
      const response = await apiService.sendQuery(input);
    
      responseMessage.text = JSON.stringify(response.data);
    } catch {
      responseMessage.text = 'Error: Something went wrong';
    }
  
    setMessages([...messages, userMessage, responseMessage]);
    
    setInput('');  // Clear the input field
  };

  return (
    <div className="chatbox">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-section">
        <input
          type="text"
          value={input}
          onChange={(e) => { setInput(e.target.value); }}
          onKeyDown={async (e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask me something..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbox;
