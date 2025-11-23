document.getElementById("checkBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "⏳ Checking...";

  try {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await res.json();
    const prob = (data.prob_phishing * 100).toFixed(2);

    if (data.label === 1) {
      resultDiv.innerHTML = `🚨 <b>Phishing!</b><br>Probability: ${prob}%`;
      resultDiv.style.color = "red";
    } else {
      resultDiv.innerHTML = `✅ <b>Safe!</b><br>Probability: ${prob}%`;
      resultDiv.style.color = "green";
    }
  } catch (err) {
    resultDiv.innerHTML = "❌ API not reachable. Start your FastAPI server!";
  }
});
