import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Loader3 } from "./Loaders";
import "./Demo.css";

function generateUniqueKey(prefix, index) {
  return `${prefix}${index + 1}`;
}

function Demo() {
  const { state } = useLocation();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulación de una llamada asíncrona para obtener los datos
    setTimeout(() => {
      setIsLoading(false);
    }, 2000);
  }, []);

  if (isLoading) {
    return <Loader3 />;
  }

  let resultClass = "";
  let resultColor = "";

  switch (state.respuesta) {
    case "Verdadera":
      resultClass = "verdadera";
      resultColor = "#008000";
      break;
    case "Falsa":
      resultClass = "falsa";
      resultColor = "#ff0000";
      break;
    case "Parcialmente verdadera":
      resultClass = "parcialmente-verdadera";
      resultColor = "#ffa500";
      break;
    case "Sin información suficiente":
      resultClass = "sin-informacion";
      resultColor = "#808080";
      break;
    default:
      resultClass = "sin-informacion";
      break;
  }

  return (
    <div className="container_llm">
      <div className="content_llm">
        <h2 className="title_result_llm">Verificación de la noticia</h2>
        <div className="result_llm">
          <p>
            <strong>Noticia:</strong> {state.texto}
          </p>
          <p className="resultado_state_llm">
            <strong>Resultado: &nbsp; </strong>
            <div className={`${resultClass}`} style={{ color: resultColor }}>
              <strong>
                {state.respuesta
                  ? state.respuesta
                  : "Sin información suficiente"}
              </strong>
            </div>
          </p>
          <div>
            <strong>Validación con LLM:</strong>
            {state.reason.split("\n").map((line, index) => (
              <p key={generateUniqueKey("line", index)}>{line}</p>
            ))}
          </div>
          <div>
            <strong>Fuentes analizadas:</strong>
            {state.fuentes.map((fuente, index) => (
              <p key={generateUniqueKey("fuente", index)}>
                -{" "}
                <a className="title" href={fuente.source}>
                  {fuente.title}
                </a>
              </p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Demo;
