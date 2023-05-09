import './App.css';
import NewsChecker from './Components/NewsChecker';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SourcesPage from './Components/SourcesPage';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <h1>RealCheck</h1>
        <Routes>
          <Route exact path="/" element={<NewsChecker />} />
          <Route path="/sources" element={<SourcesPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
