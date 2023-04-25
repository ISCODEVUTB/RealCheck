import React, { useState } from "react";
import "./NewsChecker.css";

function NewsChecker() {
  const [inputText, setInputText] = useState("");
  const [resultText, setResultText] = useState("");
  const [veri, setVeri] = useState(0);
  const [showResult, setShowResult] = useState(false);

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch("http://172.190.53.35:5000/verificar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto: inputText }),
    })
      .then((response) => response.json())
      .then((data) => {
        let message;
        if (data.verificabilidad === 0) {
          message = `La oración no se puede verificar con una probabilidad del ${(data.probabilidad[0]*100).toFixed(2)}%.`;
        } else if (data.verificabilidad === 1) {
          message = `La oración que ingresaste se puede verificar con una probabilidad del ${(data.probabilidad[1]*100).toFixed(2)}%.`;
        } else {
          message = `Verificabilidad: ${data.verificabilidad}, Probabilidad: ${data.probabilidad}`;
        }
        setResultText(message);
        setVeri(data.verificabilidad);
        setShowResult(true);
      });
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
            Verificar
          </button>
        </div>
      </form>
      <div className={showResult ? "result-container" : ""}>
        <p className={`result-text${veri === 0 ? " no" : ""}`}>
          {resultText}
        </p>
      </div>
    </div>
  );
}

export default NewsChecker;
