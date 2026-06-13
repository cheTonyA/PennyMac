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

const latestTickerEl = document.getElementById("latestTicker");
const latestMoveEl = document.getElementById("latestMove");
const latestCloseEl = document.getElementById("latestClose");

let moversChart = null;

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

function normalizeMovers(movers) {
  return movers
    .map((mover) => ({
      trade_date: mover.trade_date,
      ticker: mover.ticker,
      close: Number(mover.close),
      percent_change: Number(mover.percent_change)
    }))
    .sort((a, b) => new Date(a.trade_date) - new Date(b.trade_date));
}

function renderSummaryCards(movers) {
  if (!movers || movers.length === 0) {
    latestTickerEl.textContent = "--";
    latestMoveEl.textContent = "--";
    latestCloseEl.textContent = "--";
    return;
  }

  const latest = [...movers].sort(
    (a, b) => new Date(b.trade_date) - new Date(a.trade_date)
  )[0];

  const percentClass = latest.percent_change >= 0 ? "positive" : "negative";

  latestTickerEl.textContent = latest.ticker;
  latestMoveEl.textContent = `${latest.percent_change.toFixed(2)}%`;
  latestMoveEl.className = percentClass;
  latestCloseEl.textContent = `$${latest.close.toFixed(2)}`;
}

function renderChart(movers) {
  const chartCanvas = document.getElementById("moversChart");

  const labels = movers.map((mover) => `${mover.trade_date} ${mover.ticker}`);
  const values = movers.map((mover) => mover.percent_change);

  const barColors = values.map((value) =>
    value >= 0 ? "rgba(34, 197, 94, 0.75)" : "rgba(239, 68, 68, 0.75)"
  );

  const borderColors = values.map((value) =>
    value >= 0 ? "rgba(34, 197, 94, 1)" : "rgba(239, 68, 68, 1)"
  );

  if (moversChart) {
    moversChart.destroy();
  }

  moversChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Percent Change",
          data: values,
          backgroundColor: barColors,
          borderColor: borderColors,
          borderWidth: 1,
          borderRadius: 8
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: "#cbd5e1"
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const mover = movers[context.dataIndex];
              return `${mover.ticker}: ${mover.percent_change.toFixed(2)}% close $${mover.close.toFixed(2)}`;
            }
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: "#94a3b8",
            maxRotation: 45,
            minRotation: 0
          },
          grid: {
            color: "rgba(148, 163, 184, 0.12)"
          }
        },
        y: {
          ticks: {
            color: "#94a3b8",
            callback: (value) => `${value}%`
          },
          grid: {
            color: "rgba(148, 163, 184, 0.12)"
          }
        }
      }
    }
  });
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

  const newestFirst = [...movers].sort(
    (a, b) => new Date(b.trade_date) - new Date(a.trade_date)
  );

  newestFirst.forEach((mover) => {
    const percentClass = mover.percent_change >= 0 ? "positive" : "negative";
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${mover.trade_date}</td>
      <td class="ticker">${mover.ticker}</td>
      <td>$${mover.close.toFixed(2)}</td>
      <td class="${percentClass}">${mover.percent_change.toFixed(2)}%</td>
    `;

    tableBody.appendChild(row);
  });
}

async function loadMovers() {
  try {
    statusEl.textContent = API_URL
      ? "Fetching latest mover data..."
      : "Using local mock data for frontend preview.";

    const rawMovers = await fetchMovers();
    const movers = normalizeMovers(rawMovers);

    renderSummaryCards(movers);
    renderChart(movers);
    renderMovers(movers);

    statusEl.textContent = API_URL
      ? "Live data loaded from API Gateway."
      : "Preview mode: mock data loaded.";
  } catch (error) {
    console.error(error);

    statusEl.textContent = "Failed to load mover data.";

    renderSummaryCards([]);
    tableBody.innerHTML = `
      <tr>
        <td colspan="4" class="empty">Unable to fetch data.</td>
      </tr>
    `;
  }
}

refreshBtn.addEventListener("click", loadMovers);

loadMovers();