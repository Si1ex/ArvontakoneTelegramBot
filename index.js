const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = process.env.PORT || 3000;

const pythonBotScript = 'main.py';
const pythonExecutable = '"C:\\Python310\\python.exe"'; // Use double quotes and backslashes

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);

  const pythonBotProcess = exec(`${pythonExecutable} ${pythonBotScript}`);

  pythonBotProcess.stdout.on('data', (data) => {
    console.log(`Bot stdout: ${data}`);
  });

  pythonBotProcess.stderr.on('data', (data) => {
    console.error(`Bot stderr: ${data}`);
  });

  pythonBotProcess.on('close', (code) => {
    console.log(`Bot process exited with code ${code}`);
  });
});