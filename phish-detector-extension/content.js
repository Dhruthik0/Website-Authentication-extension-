(async () => {
  const url = window.location.href;
  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    const result = await response.json();

    const prob = (result.prob_phishing * 100).toFixed(2);
    const label = result.label ? "⚠️ Phishing suspected!" : "✅ Safe website";

    alert(`${label}\nPhishing probability: ${prob}%`);
  } catch (error) {
    console.error("Error:", error);
    alert("❌ Could not check this URL. Is the API running?");
  }
})();
