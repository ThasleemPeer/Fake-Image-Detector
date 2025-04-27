import React from "react";
import UploadForm from "./components/UploadForm";
import "./index.css";

function App() {
  return (
    <div className="App">
      <header>
        <h1>Fake Image Detector</h1>
      </header>
      <main>
        <UploadForm />
      </main>
    </div>
  );
}

export default App;
