const express = require("express");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
const fs = require("fs");
const FormData = require("form-data");

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: "storage/" });

app.post("/api/tts", upload.single("voice_sample"), async (req, res) => {
  const { text } = req.body;
  const voiceSample = req.file;

  const formData = new FormData();
  formData.append("voice_sample", fs.createReadStream(voiceSample.path));
  formData.append("text", text);

  try {
    const response = await axios.post(
      "http://inference:8000/generate",
      formData,
      {
        headers: formData.getHeaders(),
        responseType: "stream",
      }
    );
    res.setHeader("Content-Type", "audio/wav");
    response.data.pipe(res);
  } catch (err) {
    console.error(err);
    res.status(500).send("Error generating voice");
  }
});

app.listen(3001, () => console.log("Node API running on port 3001"));
