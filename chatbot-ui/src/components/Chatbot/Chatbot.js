// src/components/Chatbot/Chatbot.js

import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (input) => {
    if (input.trim() !== '') {
      const userMessage = { text: input, sender: 'user' };
      setMessages(messages => [...messages, userMessage]);

      // Simulate API call for bot response
      const botResponse = await getBotResponse(input);
      const botMessage = { text: botResponse, sender: 'bot' };
      setMessages(messages => [...messages, botMessage]);
    }
  };

  const getBotResponse = async (input) => {
    try {
      const response = await fetch('/api/gateway', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input_data: input })
      });
  
      if (response.ok) {
        const responseData = await response.json();
        return responseData.message;  // Assuming the response has a 'message' field
      } else {
        console.error('API response error:', response.status);
        return 'Sorry, I encountered an error.';
      }
    } catch (error) {
      console.error('Network error:', error);
      return 'Sorry, there was a network error.';
    }
  };
  

  const handleSendMessage = (e) => {
    e.preventDefault();
    const input = e.target.elements.messageInput.value;
    sendMessage(input);
    e.target.elements.messageInput.value = '';
  };

  return (
    <div className="chatbot">
      <div className="chatbot-header">
        <h1>ConvoCrafter</h1>
      </div>
      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form className="chatbot-input" onSubmit={handleSendMessage}>
        <input
          type="text"
          name="messageInput"
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chatbot;
