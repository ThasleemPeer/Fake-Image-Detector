import React, { useState } from "react";
import axios from "axios";

const UploadForm = () => {
  const [image, setImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    setIsLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await axios.post("http://localhost:8000/api/image/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const data = response.data;
      setResult({
        isFake: data.is_fake,
        confidence: data.confidence,
        message: data.is_fake ? "Fake Image" : "Real Image",
      });
    } catch (error) {
      console.error("Error uploading image:", error);
      setResult({ message: "Error processing the image" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Fake Image Detection</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Processing..." : "Upload Image"}
        </button>
      </form>

      {result && (
        <div className={`result ${result.isFake ? "error" : "success"}`}>
          <h2>{result.message}</h2>
          <p>Confidence: {result.confidence}%</p>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
