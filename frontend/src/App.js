import { BrowserRouter, Routes, Route } from "react-router-dom";
import AIChatbotHome from "./Pages/AIChatbotHome";
import LegalAIAssistant from "./Pages/LegalAIAssistant";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AIChatbotHome />} />
        <Route path="/chat" element={<LegalAIAssistant />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
