import React, { useState } from "react";
import "./NewsChecker.css";

function NewsChecker() {
  const [inputText, setInputText] = useState("");
  const [resultText, setResultText] = useState("");

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch("http://localhost:5000/verificar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto: inputText }),
    })
      .then((response) => response.json())
      .then((data) => setResultText(`Verificabilidad: ${data.verificabilidad}, Probabilidad: ${data.probabilidad}`));
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <input
            className="input-field"
            type="text"
            value={inputText}
            onChange={handleInputChange}
          />
          <button className="submit-button" type="submit">
            Comprobar
          </button>
        </div>
      </form>
      <p>{resultText}</p>
    </div>
  );
}

export default NewsChecker;
