import { useLocation } from "react-router-dom";
import './SourcesPage.css';

function SourcesPage() {

  const { state } = useLocation();
  //console.log("Sources: ", state.sources)
  //console.log("Preprocesado:", state.preprocesado.join(", "))

  const sourcesList = state.sources.map((source) => {
    return (
      <div className="card" key={source._id}>
        <div className="column">
          <p className="id">{source._id}</p>
        </div>
        <div className="column-content">
          <a className="title" href={source.source}>{source.title}</a>
          <p className="descsription">{source.description}</p>
        </div>
        <div className="column">
          <p className="verifying">Verificando...</p>
        </div>
      </div>
    );
  });

  return (
    <div>
      <h2 className="cont-title">Fuentes encontradas</h2>
      <p className="cont-subtitle">Texto preprocesado: {state.preprocesado.join(", ")}</p>
      <div className="card-container">
        {sourcesList}
      </div>
    </div>
  );
}

export default SourcesPage;
