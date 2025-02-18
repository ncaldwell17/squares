import React from "react";
import SquaresContainer from "@/components/SquaresContainer.tsx";
import {BrowserRouter, Routes, Route} from "react-router-dom";

const App: React.FC = () => {
  return (
      <BrowserRouter>
          <Routes>
              <Route path={"/"} element={<SquaresContainer />} />
          </Routes>
      </BrowserRouter>
  );
};

export default App;
