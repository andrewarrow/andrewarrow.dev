function log(msg) {
  document.getElementById("log").innerText = msg;
}

function formatResult(result) {
  if (typeof result === 'string') {
    try {
      // Try to parse as JSON if it's a string
      const parsed = JSON.parse(result);
      return JSON.stringify(parsed, null, 2);
    } catch {
      // If not JSON, return as is
      return result;
    }
  } else if (typeof result === 'object') {
    // If it's already an object, stringify it with formatting
    return JSON.stringify(result, null, 2);
  }
  return String(result);
}

function requestAgeRange() {
  if (!window.AppleAgeRange) {
    log("Age Range API unavailable");
    return;
  }

  window.AppleAgeRange.request()
    .then(result => log("Age Range:\n" + formatResult(result)))
    .catch(err => log("Error: " + err));
}

function purchaseItem() {
  if (!window.AppleCommerce) {
    log("Purchase API unavailable");
    return;
  }

  window.AppleCommerce.purchase({
    productId: "DEMO_001",
    description: "Demo Purchase"
  })
    .then(result => log("Purchase Success:\n" + formatResult(result)))
    .catch(err => log("Purchase Failed: " + err));
}

function getHostVersion() {
  if (!window.AppHost) {
    log("Host API unavailable");
    return;
  }

  window.AppHost.version()
    .then(result => log("Host Version:\n" + formatResult(result)))
    .catch(err => log("Error: " + err));
}