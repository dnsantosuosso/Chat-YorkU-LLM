import React, { useState, useRef } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Stack,
  // CircularProgress,
} from '@mui/material';
import axios from 'axios';

const Chat = () => {
  const [formData, setFormData] = useState({
    message: '',
  });
  const [messages, setMessages] = useState([]);
  // const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);

  const sendMsg = async () => {
    try {
      const newMessage = {
        id: Date.now(),
        message: formData.message,
        isUser: true,
        ts: Date.now(),
      };
      setMessages([...messages, newMessage]);
      setFormData({ message: '' });
      scrollToBottom();

      const response = await axios.post('http://206.12.88.44:5000/Answer', {
        question: formData.message,
      });

      const assistant_message = response.data.answer
        .split('<|assistant|>')[1]
        .trim();

      const botResponse = {
        id: Date.now(),
        message: assistant_message,
        isUser: false,
        ts: Date.now(),
      };

      setMessages((prevMessages) => [...prevMessages, botResponse]);
      scrollToBottom();
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  return (
    <Box
      sx={{
        margin: '10px',
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
      }}
    >
      <Box
        sx={{
          overflowY: 'auto',
          height: 'calc(100% - 180px)',
          p: 2,
          mt: 8,
          mb: 30,
        }}
      >
        {messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              mt: 1,
              border: '1px solid #ccc',
              p: 2,
              position: 'relative',
              textAlign: 'left', // Always set to 'left' to ensure both user and bot messages are on the left
            }}
          >
            <Typography>
              {message.isUser ? <strong>You:</strong> : <strong>Bot:</strong>}{' '}
              {message.message}
            </Typography>
          </Box>
        ))}

        <div ref={messagesEndRef} />
      </Box>
      <Box
        sx={{
          position: 'fixed',
          bottom: 0,
          width: '100%',
          backgroundColor: '#fff',
          zIndex: 1,
          boxShadow: '0 -2px 4px rgba(0,0,0,0.1)',
          p: 2,
        }}
      >
        <Stack direction="row" spacing={2} sx={{ mb: 2, marginRight: '40px' }}>
          <TextField
            label="Message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            variant="outlined"
            multiline
            fullWidth
            sx={{ mb: 2 }}
          />
          <Button variant="contained" onClick={sendMsg}>
            Send
          </Button>
        </Stack>
      </Box>
    </Box>
  );
};

export default Chat;
