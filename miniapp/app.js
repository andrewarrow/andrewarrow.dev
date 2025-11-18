function log(msg) {
  document.getElementById("log").innerText = msg;
}

function requestAgeRange() {
  if (!window.AppleAgeRange) {
    log("AgeRange API unavailable");
    return;
  }

  window.AppleAgeRange.request()
    .then(result => log("Age Range: " + JSON.stringify(result)))
    .catch(err => log("Error: " + err));
}

function purchaseItem() {
  if (!window.AppleCommerce) {
    log("Purchase API unavailable");
    return;
  }

  window.AppleCommerce.purchase({
    productId: "demo_product_1",
    description: "Demo Purchase"
  })
    .then(result => log("Purchase Success: " + JSON.stringify(result)))
    .catch(err => log("Purchase Failed: " + err));
}

function getHostVersion() {
  if (!window.AppHost) {
    log("Host API unavailable");
    return;
  }

  window.AppHost.version()
    .then(v => log("Host Version: " + v))
    .catch(err => log(err));
}