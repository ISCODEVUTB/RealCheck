import React, { useState } from "react";
import "./NewsChecker.css";
import { useNavigate } from "react-router-dom";

function NewsChecker() {
  const navigate = useNavigate();
  const [inputText, setInputText] = useState("");
  const [resultText, setResultText] = useState("");
  const [veri, setVeri] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [showButton, setShowButton] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [dotsCount, setDotsCount] = useState(0);

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
          message = `Hay una probabilidad del ${(data.probabilidad[0]*100).toFixed(2)}% de que el texto que ingresaste sea un comentario.`;
        } else if (data.verificabilidad === 1) {
          message = `Hay una probabilidad del ${(data.probabilidad[1]*100).toFixed(2)}% de que el texto que ingresaste sea un titular de noticia.`;
          setShowButton(true); // Mostrar el botón "Buscar fuentes"
        } else {
          message = `Verificabilidad: ${data.verificabilidad}, Probabilidad: ${data.probabilidad}`;
        }
        setResultText(message);
        setVeri(data.verificabilidad);
        setShowResult(true);
      });
  };

  const handleSearchClick = (text) => {
    setIsLoading(true); // Establecer isLoading como true
    setDotsCount(0); // Inicializar el contador de puntos a cero
    const intervalId = setInterval(() => {
      // Actualizar el contador de puntos
      setDotsCount((count) => (count + 1) % 4);
    }, 500);
    fetch("http://172.190.53.35:5000/search", { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto: text }),
    })
      .then((response) => response.json())
      .then((data) => {
        clearInterval(intervalId); // Limpiar el intervalo cuando la búsqueda se completa
        setIsLoading(false); // Establecer isLoading como false
        console.log("Texto: ", text)
        console.log("Sources: ", data.sources)
        console.log("Preprocesado:", data.preprocesado)
        const state = {
          texto: text,
          sources: data.sources,
          preprocesado: data.preprocesado
        };
        navigate('/sources', { state });
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
        <div className="button-container">
          {showButton && (
            <button className="button-sources" onClick={() => handleSearchClick(inputText)} disabled={isLoading}>
              {isLoading ? `Cargando${'.'.repeat(dotsCount)}` : "Buscar fuentes"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default NewsChecker;
