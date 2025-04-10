import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./pages/Home";
import Question from "./pages/Question";
import Results from "./pages/Results";

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/question/:id" element={<Question />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </Router>
  );
}

export default App;
