chrome.permissions.contains(
  {
    permissions: ["cookies", "tabs", "activeTab"],
    origins: ["https://daparto.de/*", "https://www.daparto.de/*"],
  },
  function (result) {
    if (result) {
      console.log("All permissions granted");
    } else {
      console.log("Missing permissions");
    }
  }
);

const findPartsBtn = document.getElementById("findPartsBtn");
const resetBtn = document.getElementById("resetBtn");
const errorDiv = document.getElementById("error");
const resultDiv = document.getElementById("result");
const partInput = document.getElementById("partInput");
// Reset button clears all states
resetBtn.addEventListener("click", function () {
  partInput.value = "";
  setResult("");
  setError("");
  localStorage.removeItem("partInput");
  localStorage.removeItem("resultDiv");
  localStorage.removeItem("errorDiv");
});

// Restore state on load
window.addEventListener("DOMContentLoaded", function () {
  partInput.value = localStorage.getItem("partInput") || "";
  resultDiv.innerHTML = localStorage.getItem("resultDiv") || "";
  errorDiv.innerHTML = localStorage.getItem("errorDiv") || "";
  errorDiv.style.display = errorDiv.innerHTML ? "block" : "none";
});

// Save textarea on input
partInput.addEventListener("input", function () {
  localStorage.setItem("partInput", partInput.value);
});

// Helper functions to set and persist result/error
function setResult(html) {
  resultDiv.innerHTML = html;
  localStorage.setItem("resultDiv", html);
}
function setError(html) {
  errorDiv.innerHTML = html;
  errorDiv.style.display = html ? "block" : "none";
  localStorage.setItem("errorDiv", html);
}

findPartsBtn.addEventListener("click", function () {
  const partNumbers = partInput.value.trim();
  if (!partNumbers) {
    setError("Please enter a part number.");
    return;
  }
  setError("");
  setResult("");
  findPartsBtn.disabled = true;
  findPartsBtn.textContent = "Loading...";
  // Store the part number for use in the message handler
  findPartsBtn.dataset.partNumbers = partNumbers;
  // Ask background to send cf_clearance cookie
  chrome.runtime.sendMessage({ type: "get_cf_clearance_cookie" });
});

// Listen for cf_clearance cookie from background
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg && msg.type === "cf_clearance_cookie") {
    setError("");
    // Send to backend API
    const partNumbers = findPartsBtn.dataset.partNumbers || "";
    fetch("http://localhost:5000/trigger", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cf_clearance_cookie: msg.value,
        domain: msg.domain,
        partitionKey: msg.partitionKey,
        part_number: partNumbers,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          setResult(`<div class="success">${data.message}</div>`);
        } else {
          setResult(
            `<div class="error">${data.message || "Unknown error"}</div>`
          );
        }
        findPartsBtn.disabled = false;
        findPartsBtn.textContent = "Find Parts";
      })
      .catch((err) => {
        setError("Error sending to backend: " + err);
        findPartsBtn.disabled = false;
        findPartsBtn.textContent = "Find Parts";
      });
  } else if (msg && msg.type === "cf_clearance_cookie_failed") {
    setError("Failed to read cf_clearance cookie.");
    findPartsBtn.disabled = false;
    findPartsBtn.textContent = "Find Parts";
  }
});
