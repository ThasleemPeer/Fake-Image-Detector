import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const UploadForm = () => {
  const [image, setImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const resultRef = useRef(null);
  const buttonRef = useRef(null);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
    setResult(null);
  };

  const createRipple = (e) => {
    const button = buttonRef.current;
    if (!button) return;

    const ripple = document.createElement("span");
    ripple.className = "ripple";
    
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = `${size}px`;
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;

    button.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  };

  const createParticles = () => {
    if (!resultRef.current || result?.isFake) return;

    const container = resultRef.current;
    const particlesContainer = document.createElement("div");
    particlesContainer.className = "particles";
    
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement("div");
      particle.className = "particle";
      
      // Random position and animation
      const angle = Math.random() * Math.PI * 2;
      const distance = 20 + Math.random() * 50;
      const tx = Math.cos(angle) * distance;
      const ty = Math.sin(angle) * distance;
      
      particle.style.setProperty('--tx', `${tx}px`);
      particle.style.setProperty('--ty', `${ty}px`);
      particle.style.left = `${50 + Math.cos(angle) * 10}%`;
      particle.style.top = `${50 + Math.sin(angle) * 10}%`;
      particle.style.animationDelay = `${Math.random() * 0.5}s`;
      particle.style.backgroundColor = i % 2 === 0 ? "#4ade80" : "#a7f3d0";
      particle.style.width = particle.style.height = `${4 + Math.random() * 4}px`;
      
      particlesContainer.appendChild(particle);
    }
    
    container.appendChild(particlesContainer);
    
    setTimeout(() => {
      particlesContainer.remove();
    }, 1000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    setIsLoading(true);
    setResult(null);

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

  useEffect(() => {
    if (result) {
      createParticles();
    }
  }, [result]);

  return (
    <div className="upload-container">
      <h1 className="upload-title">Fake Image Detection</h1>

      <form onSubmit={handleSubmit} className={`upload-form ${isLoading ? "uploading" : ""}`}>
        <div className="file-input-wrapper">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            disabled={isLoading}
            className="file-input"
          />
        </div>
        <button
          ref={buttonRef}
          type="submit"
          disabled={isLoading}
          className="submit-btn"
          onClick={createRipple}
        >
          {isLoading ? (
            <>
              <span className="spinner"></span>
              Processing...
            </>
          ) : (
            "Upload Image"
          )}
        </button>
      </form>

      {result && (
        <div
          ref={resultRef}
          className={`result-container ${
            result.isFake ? "result-fake fake-animation" : "result-real real-animation"
          } result-show`}
        >
          <h2 className="result-message">{result.message}</h2>
          <p className="result-confidence">Confidence: {result.confidence}%</p>
          <div className="result-icon">
            {result.isFake ? "❌" : "✅"}
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadForm;