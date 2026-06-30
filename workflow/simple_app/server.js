const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

// Node endpoint
app.post("/send", async (req, res) => {
  try {
    const userInput = req.body.text;

    // send to FastAPI
    const response = await axios.post("http://localhost:8000/process", {
      text: userInput
    });

    // return FastAPI result
    res.json({
      fromNode: true,
      result: response.data.processed
    });

  } catch (err) {
    res.status(500).json({ error: "Something went wrong" });
  }
});

app.listen(3000, () => {
  console.log("Node server running on http://localhost:3000");
});