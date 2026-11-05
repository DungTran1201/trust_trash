document.getElementById("capture").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  const result = document.getElementById("result");
  result.textContent = JSON.stringify({ title: tab?.title ?? null, url: tab?.url ?? null }, null, 2);
});
