// Function to extract cf_clearance cookie with partitionKey and send to popup
function sendCfClearanceCookieToPopup() {
  chrome.cookies.getAll({ partitionKey: {} }, function (cookies) {
    const cfCookie = cookies.find((cookie) => cookie.name === "cf_clearance");
    if (cfCookie) {
      chrome.runtime.sendMessage({
        type: "cf_clearance_cookie",
        value: cfCookie.value,
        domain: cfCookie.domain,
        partitionKey: cfCookie.partitionKey,
      });
    }
  });
}

// Listen for popup requesting the cookie
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "get_cf_clearance_cookie") {
    sendCfClearanceCookieToPopup();
  }
});
chrome.cookies.getAll({ partitionKey: {} }, function (theCookies) {
  cookies = theCookies;
  console.log(cookies);
});
