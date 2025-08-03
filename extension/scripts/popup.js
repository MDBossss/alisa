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
const errorDiv = document.getElementById("error");
const resultDiv = document.getElementById("result");
const partInput = document.getElementById("partInput");

findPartsBtn.addEventListener("click", function () {
  const partNumber = partInput.value.trim();
  if (!partNumber) {
    errorDiv.textContent = "Please enter a part number.";
    errorDiv.style.display = "block";
    return;
  }
  errorDiv.style.display = "none";
  resultDiv.innerHTML = "";
  findPartsBtn.disabled = true;
  findPartsBtn.textContent = "Loading...";
  // Store the part number for use in the message handler
  findPartsBtn.dataset.partNumber = partNumber;
  // Ask background to send cf_clearance cookie
  chrome.runtime.sendMessage({ type: "get_cf_clearance_cookie" });
});

// Listen for cf_clearance cookie from background
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg && msg.type === "cf_clearance_cookie") {
    errorDiv.style.display = "none";
    // Send to backend API
    const partNumber = findPartsBtn.dataset.partNumber || "";
    fetch("http://localhost:5000/trigger", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cf_clearance_cookie: msg.value,
        domain: msg.domain,
        partitionKey: msg.partitionKey,
        part_number: partNumber,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          resultDiv.innerHTML = `<div class="success">${data.message}</div>`;
        } else {
          resultDiv.innerHTML = `<div class="error">${
            data.message || "Unknown error"
          }</div>`;
        }
        findPartsBtn.disabled = false;
        findPartsBtn.textContent = "Find Parts";
      })
      .catch((err) => {
        errorDiv.textContent = "Error sending to backend: " + err;
        errorDiv.style.display = "block";
        findPartsBtn.disabled = false;
        findPartsBtn.textContent = "Find Parts";
      });
  } else if (msg && msg.type === "cf_clearance_cookie_failed") {
    errorDiv.textContent = "Failed to read cf_clearance cookie.";
    errorDiv.style.display = "block";
    findPartsBtn.disabled = false;
    findPartsBtn.textContent = "Find Parts";
  }
});
