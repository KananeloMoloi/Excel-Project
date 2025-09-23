const express = require("express");
const multer = require("multer");
const axios = require("axios");
const fs = require("fs");
const path = require("path");
const FormData = require("form-data");

const app = express();
const upload = multer({ dest: "uploads/" });

// Serve static files
app.use(express.static(__dirname));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/upload", upload.single("excel"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const filePath = req.file.path;
    const userId = 1; // example user id

    console.log(" Upload received:", req.file.originalname);

    //  Prepare FormData correctly
    const formData = new FormData();
    formData.append("file", fs.createReadStream(filePath)); // must match FastAPI's "file"

    console.log(" Sending file to FastAPI...");

    const pythonUpload = await axios.post(
      `http://127.0.0.1:8000/upload-excel/${userId}`,
      formData,
      {
        headers: formData.getHeaders(),
        maxBodyLength: Infinity, // handle large files
      }
    );

    console.log("FastAPI response:", pythonUpload.data);

    fs.unlink(filePath, () => {}); // clean up temp file

    res.json(pythonUpload.data);
  } catch (err) {
    console.error(" UPLOAD ERROR:", err.response?.data || err.message);
    res.status(500).json({
      error: "Upload failed",
      details: err.response?.data || err.message,
    });
  }
});

app.listen(3000, () => {
  console.log(" Frontend server running at http://localhost:3000");
});
