function startScan() {
  const scanBtn = document.getElementById("scanBtn");
  const status = document.getElementById("scan-status");

  scanBtn.disabled = true;
  scanBtn.innerText = "🔄 Scanning...";
  status.textContent = "Scanning in progress...";

  fetch("/launch-scan")
    .then(response => {
      if (!response.ok) throw new Error("Scan failed");
      return response.json();
    })
    .then(data => {
      scanBtn.disabled = false;
      scanBtn.innerText = "🔍 Scan Again";
      status.textContent = `✅ Scan complete! ${data.devices} devices found.`;
      setTimeout(() => location.reload(), 1000); // refresh page after 1s
    })
    .catch(err => {
      status.textContent = "❌ Scan failed";
      scanBtn.disabled = false;
      scanBtn.innerText = "🔍 Scan Now";
      console.error(err);
    });
}

function filterTable() {
  const input = document.getElementById("searchInput");
  const filter = input.value.toLowerCase();
  const table = document.getElementById("scanTable");
  const rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    let show = false;
    const cells = rows[i].getElementsByTagName("td");
    for (let j = 0; j < cells.length; j++) {
      const txt = cells[j].textContent || cells[j].innerText;
      if (txt.toLowerCase().indexOf(filter) > -1) {
        show = true;
        break;
      }
    }
    rows[i].style.display = show ? "" : "none";
  }
}
