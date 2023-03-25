import React, { useState, useRef, useEffect } from "react";
import "./Console.css";

function Console({ sendInputToCode, output, width, codeIsRunning }) {
  const [inputValue, setInputValue] = useState(""); // Initialize input value to an empty string
  const consoleRef = useRef(null); // Create a ref to the console output element

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      sendInputToCode(inputValue + "\n"); // Send input to the parent component
      setInputValue(""); // Reset input value
    }
  };

  const handleChange = (event) => {
    setInputValue(event.target.value); // Update input value as the user types
  };

  useEffect(() => {
    // Scroll the console to the bottom whenever the output changes
    consoleRef.current.scrollTop = consoleRef.current.scrollHeight - consoleRef.current.clientHeight;
  }, [output]);

  return (
    <div
      className="output-container"
      style={{ width: `calc(100% - ${width}px)` }} // Set the width of the console
      tabIndex={0}
    >
      <div ref={consoleRef} className="console" style={{ height: "calc(100% - 45px)", whiteSpace: "pre", fontFamily: "monospace" }}>{output}</div>
      <input
        className="input-bar"
        style={{
          width: `calc(100% - ${width}px - 35px)`, // Set the width of the input bar
          cursor: codeIsRunning ? "auto" : "not-allowed", // Change the cursor style based on whether code is running or not
          backgroundColor: codeIsRunning ? "#3a4144" : "#2e3237" // Change the background color based on whether code is running or not
        }}
        type="text"
        value={inputValue}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        disabled={!codeIsRunning} // Disable the input bar when code is not running
        placeholder={!codeIsRunning ? "" : "Input goes here..."}
      ></input>
    </div>
  )
}

export default Console;
