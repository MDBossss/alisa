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

document.getElementById("readCookieBtn").addEventListener("click", function () {
  // Ask background to send cf_clearance cookie
  chrome.runtime.sendMessage({ type: "get_cf_clearance_cookie" });
});

// Listen for cf_clearance cookie from background
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg && msg.type === "cf_clearance_cookie") {
    let html = `<strong>cf_clearance cookie was read:</strong><br>`;
    html += `<code>${msg.value}</code><br>`;
    html += `<small>Domain: ${msg.domain}, PartitionKey: ${JSON.stringify(
      msg.partitionKey
    )}</small>`;
    document.getElementById("cookieValue").innerHTML = html;
  }
});
