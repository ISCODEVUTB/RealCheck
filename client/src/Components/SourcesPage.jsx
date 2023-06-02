import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./SourcesPage.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { Loader2, Loader3 } from "./Loaders";

function SourcesPage() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const [probabilities, setProbabilities] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [hasFetchedData, setHasFetchedData] = useState(false);
  const [isLoadingVer, setIsLoadingVer] = useState(false);
  const titularesSeleccionados = [];

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
          console.log("Se hace petición: ", hasFetchedData);
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

  const handleLLMClick = async (text) => {
    setIsLoadingVer(true); // Establecer isLoading como true
    console.log("Analizar...");
    console.log("Fuentes escogidas: ", titularesSeleccionados);

    try {
      const response = await fetch("http://172.190.53.35:5000/check_llm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          texto: text,
          fuentes_escogidas: titularesSeleccionados,
        }),
      });

      const data = await response.json();

      setIsLoadingVer(false); // Establecer isLoading como false
      console.log("Texto: ", text);
      console.log("Respuesta: ", data.res);
      console.log("Razón:", data.reason);
      console.log("Fuentes analizada 1: ", data.fuentes[0].title);
      console.log("Fuentes analizada 2: ", data.fuentes[1].title);

      const state = {
        texto: text,
        respuesta: data.res,
        reason: data.reason,
        fuentes: data.fuentes,
      };

      navigate("/demo", { state });
    } catch (error) {
      console.error("Error:", error);
      setIsLoadingVer(false); // Establecer isLoading como false en caso de error
    }
  };

  // Renderizar el contenido normalmente si isLoading es falso
  const sourcesList = state.sources.map((source) => {
    let is_selected = false;
    let status = "No seleccionado";
    if (probabilities?.titulares_seleccionados?.includes(source.title)) {
      status = "Seleccionado";
      is_selected = true;
      titularesSeleccionados.push(source);
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
    <div className="contenedor_sources">
      <h2 className="cont-title">Fuentes encontradas</h2>
      <button
        className="button-sources"
        onClick={() => handleLLMClick(state.texto)}
        disabled={isLoadingVer}
      >
        {isLoadingVer ? <Loader2 /> : "Verificar con LLM"}
      </button>
      <p className="cont-subtitle">
        Noticia preprocesada: {state.preprocesado.join(", ")}
      </p>
      <div className="card-container">{sourcesList}</div>
    </div>
  );
}

export default SourcesPage;
