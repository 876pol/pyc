import React, { useState, useCallback } from "react";
import Editor from "./components/Editor";
import Header from "./components/Header";
import Console from "./components/Console";
import "./App.css";

var socket = null;

function App() {
  // Initialize state variables
  const [code, setCode] = useState("int main() {\n  return 0;\n}");
  const [output, setOutput] = useState("");
  const [width, setWidth] = useState(window.innerWidth / 2);
  const [codeIsRunning, setCodeIsRunning] = useState(false);

  // Define function to start running the code
  const startRunningCode = async () => {
    // Check if the code is too long
    if (code.length >= 50000) {
      alert("Code must be less than 50000 characters long!");
    } else {
      // Close any existing socket connections
      if (socket != null) {
        await socket.close();
      } else {
        // Create a new WebSocket connection
        socket = new WebSocket("ws://localhost:8000/ws");

        // Set up event listeners for the WebSocket connection
        socket.onopen = () => {
          setCodeIsRunning(true);
          setOutput("");
          socket.send(code);
        };
        socket.onmessage = (event) => {
          receiveOutputFromCode(JSON.parse(event.data).output);
        };
        socket.onclose = () => {
          setCodeIsRunning(false);
          socket = null;
        }
        socket.onerror = () => {
          alert("WebSocket connection failed! Try again later!");
        }
      }
    }
  };

  // Define function to receive output from the code
  const receiveOutputFromCode = useCallback((toAdd) => {
    setOutput((output) => {
      let res = output + toAdd;
      if (res.length > 10000) {
        res = res.slice(-10000);
      }
      return res;
    });
  }, []);

  // Define function to send input to the code
  const sendInputToCode = (inputValue) => {
    socket.send(inputValue);
    receiveOutputFromCode(inputValue);
  };

  // Render the app
  return (
    <div className="app">
      <Header runCode={startRunningCode} setCode={setCode} codeIsRunning={codeIsRunning} />
      <div className="main-container">
        <Editor code={code} setCode={setCode} width={width} setWidth={setWidth} />
        <Console sendInputToCode={sendInputToCode} output={output} width={width} codeIsRunning={codeIsRunning} />
      </div>
    </div>
  );
}

export default App;
