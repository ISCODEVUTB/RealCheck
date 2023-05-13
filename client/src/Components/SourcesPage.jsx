import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "./SourcesPage.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { Loader3 } from "./Loaders";

function SourcesPage() {
  const { state } = useLocation();
  const [probabilities, setProbabilities] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [hasFetchedData, setHasFetchedData] = useState(false);

  useEffect(() => {
    if (!hasFetchedData) {
      setHasFetchedData(true);
    } else {
      async function fetchData() {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            texto: state.texto,
            titulares: state.sources.map((source) => source.title),
          }),
        };

        try {
          setIsLoading(true);
          console.log("Se hace peti: ", hasFetchedData);
          const response = await fetch(
            "http://172.190.53.35:5000/check",
            requestOptions
          );
          const data = await response.json();
          console.log("Probabilidades:", data);
          setProbabilities(data);
          setIsLoading(false);
        } catch (error) {
          console.error("Error al obtener las probabilidades:", error);
        }
      }
      fetchData();
    }
  }, [state.sources, state.texto, hasFetchedData]);

  // Renderizar estado de carga si isLoading es verdadero
  if (isLoading) {
    return <Loader3 />;
  }

  // Renderizar el contenido normalmente si isLoading es falso
  const sourcesList = state.sources.map((source) => {
    let is_selected = false;
    let status = "No seleccionado";
    if (
      probabilities &&
      probabilities.titulares_seleccionados &&
      probabilities.titulares_seleccionados.includes(source.title)
    ) {
      status = "Seleccionado";
      is_selected = true;
    }
    return (
      <div className={"card"} key={source._id}>
        <div className="column">
          {is_selected ? (
            <p className="id sel">{source._id}</p>
          ) : (
            <p className="id">{source._id}</p>
          )}
        </div>
        <div className="column-content">
          <a className="title" href={source.source}>
            {source.title}
          </a>
          <p className="description">{source.description}</p>
        </div>
        <div className="column">
          <p className="verifying">
            {is_selected ? (
              <FontAwesomeIcon icon={faCheck} className="icon selected" />
            ) : (
              <FontAwesomeIcon icon={faTimes} className="icon not-selected" />
            )}
            &nbsp; {status}
          </p>
        </div>
      </div>
    );
  });

  return (
    <div>
      <h2 className="cont-title">Fuentes encontradas</h2>
      <p className="cont-subtitle">
        Texto preprocesado: {state.preprocesado.join(", ")}
      </p>
      <div className="card-container">{sourcesList}</div>
    </div>
  );
}

export default SourcesPage;
