import React, { useState } from "react";

function App() {
  const [youtubeLink, setYoutubeLink] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDownload = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/download-audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ link: youtubeLink }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const contentDisposition = response.headers.get("Content-Disposition");
        const filename = contentDisposition
          ? contentDisposition.split("filename=")[1].replace(/"/g, "")
          : "audio.mp3";

        const downloadLink = document.createElement("a");
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = filename;
        downloadLink.click();
      } else {
        setError("Erro ao baixar o áudio.");
      }
    } catch (error) {
      setError("Erro ao baixar o áudio.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div id="box">
      <h1>Conversor de Áudio do YouTube</h1>
      <input
        type="text"
        placeholder="Cole o link do vídeo do YouTube"
        value={youtubeLink}
        onChange={(e) => setYoutubeLink(e.target.value)}
      />
      <button onClick={handleDownload} disabled={isLoading}>
        {isLoading ? "Baixando..." : "Baixar Áudio"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
