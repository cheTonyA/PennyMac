const API_URL = "https://xa19nqyb68.execute-api.us-east-1.amazonaws.com/dev/movers";
const mockMovers = [
  {
    trade_date: "2026-06-10",
    ticker: "NVDA",
    close: "145.22",
    percent_change: "3.42"
  },
  {
    trade_date: "2026-06-09",
    ticker: "TSLA",
    close: "182.10",
    percent_change: "-2.15"
  },
  {
    trade_date: "2026-06-08",
    ticker: "AAPL",
    close: "204.39",
    percent_change: "1.21"
  }
];

const tableBody = document.getElementById("moversTable");
const statusEl = document.getElementById("status");
const refreshBtn = document.getElementById("refreshBtn");

async function fetchMovers() {
  if (!API_URL) {
    return mockMovers;
  }

  const response = await fetch(API_URL);

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json();
}

function renderMovers(movers) {
  tableBody.innerHTML = "";

  if (!movers || movers.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="4" class="empty">No mover data available yet.</td>
      </tr>
    `;
    return;
  }

  movers.forEach((mover) => {
    const percent = Number(mover.percent_change);
    const percentClass = percent >= 0 ? "positive" : "negative";
    const closePrice = Number(mover.close).toFixed(2);

    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${mover.trade_date}</td>
      <td class="ticker">${mover.ticker}</td>
      <td>$${closePrice}</td>
      <td class="${percentClass}">${percent.toFixed(2)}%</td>
    `;

    tableBody.appendChild(row);
  });
}

async function loadMovers() {
  try {
    statusEl.textContent = API_URL
      ? "Fetching latest mover data..."
      : "Using local mock data for frontend preview.";

    const movers = await fetchMovers();
    renderMovers(movers);

    statusEl.textContent = API_URL
      ? "Live data loaded from API Gateway."
      : "Preview mode: mock data loaded.";
  } catch (error) {
    console.error(error);
    statusEl.textContent = "Failed to load mover data.";
    tableBody.innerHTML = `
      <tr>
        <td colspan="4" class="empty">Unable to fetch data.</td>
      </tr>
    `;
  }
}

refreshBtn.addEventListener("click", loadMovers);

loadMovers();