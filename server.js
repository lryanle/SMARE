require('dotenv').config();
const express = require('express');
const { OpenAI } = require("openai");
const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post('/chatGPT', async (req, res) => {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: req.body.messages
    });
    return res.json(response);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error in OpenAI request');
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
