/* dashboard.js — Dashboard analytics and charts */

const apiBase = window.__API_BASE__ || window.location.origin || '';
let lastVendorCount = 0;

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

async function loadDashboard() {
  try {
    const [analyticsRes, forecastRes] = await Promise.all([
      fetch(`${apiBase}/api/analytics`),
      fetch(`${apiBase}/api/forecast?category=all&days=7`),
    ]);

    if (analyticsRes.ok) {
      const stats = await analyticsRes.json();
      const newVendorCount = stats.total_vendors || 0;
      const dataChanged = newVendorCount !== lastVendorCount;
      lastVendorCount = newVendorCount;

      document.getElementById('statTotal').textContent = stats.total_vendors;
      document.getElementById('statUpi').textContent = stats.vendors_with_upi;
      document.getElementById('statCities').textContent = Object.keys(stats.city_counts).length;
      document.getElementById('statBiz').textContent = Object.keys(stats.business_counts).length;

      renderCityChart(stats.city_counts, !dataChanged);
      renderBizChart(stats.business_counts, !dataChanged);
      renderVendorTable(stats.recent_vendors);
    }

    if (forecastRes.ok) {
      const forecast = await forecastRes.json();
      renderForecast(forecast);
    }

    document.querySelectorAll('.skeleton-text').forEach(el => el.classList.remove('skeleton-text'));
  } catch (e) {
    console.error('Dashboard load error:', e);
    document.querySelectorAll('.stat-val').forEach(el => el.textContent = 'Error');
    document.querySelectorAll('.skeleton-text').forEach(el => el.classList.remove('skeleton-text'));
  }
}

function renderCityChart(cityCounts, skipUpdate) {
  const ctx = document.getElementById('cityChart');
  if (!ctx) return;
  const labels = Object.keys(cityCounts);
  const data = Object.values(cityCounts);
  const colors = ['#FF6B00', '#F5C518', '#1A7A4A', '#FF5733', '#38bdf8', '#818cf8'];

  if (skipUpdate && ctx._chart) {
    ctx._chart.data.labels = labels;
    ctx._chart.data.datasets[0].data = data;
    ctx._chart.update();
    return;
  }

  if (ctx._chart) ctx._chart.destroy();
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Vendors',
        data,
        backgroundColor: colors.slice(0, labels.length),
        borderRadius: 6,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { stepSize: 1, font: { size: 11 }, color: 'rgba(255,255,255,0.5)' } },
        x: { grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { font: { size: 11 }, color: 'rgba(255,255,255,0.5)' } },
      },
    },
  });
  ctx._chart = chart;
}

function renderBizChart(bizCounts, skipUpdate) {
  const ctx = document.getElementById('bizChart');
  if (!ctx) return;
  const labels = Object.keys(bizCounts);
  const data = Object.values(bizCounts);
  const colors = ['#FF6B00', '#F5C518', '#1A7A4A', '#FF5733', '#38bdf8', '#818cf8', '#ec4899'];

  if (skipUpdate && ctx._chart) {
    ctx._chart.data.labels = labels;
    ctx._chart.data.datasets[0].data = data;
    ctx._chart.update();
    return;
  }

  if (ctx._chart) ctx._chart.destroy();
  const chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: colors.slice(0, labels.length),
        borderWidth: 2,
        borderColor: '#131619',
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { font: { size: 11 }, padding: 12, color: 'rgba(255,255,255,0.7)' },
        },
      },
    },
  });
  ctx._chart = chart;
}

function renderForecast(forecast) {
  document.getElementById('forecastSummary').textContent = forecast.summary;
  const grid = document.getElementById('forecastGrid');
  grid.innerHTML = '';

  forecast.forecast.forEach(day => {
    const pct = day.demand_index;
    const color = pct >= 80 ? '#FF5733' : pct >= 50 ? '#F5C518' : '#22A862';
    const levelClass = pct >= 80 ? 'level-high' : pct >= 50 ? 'level-medium' : 'level-low';

    const el = document.createElement('div');
    el.className = 'forecast-day';
    el.innerHTML = `
      <div class="fd-day">${day.day.slice(0, 3)}</div>
      <div class="fd-date">${day.date.slice(5)}</div>
      <div class="fd-bar">
        <div class="fd-fill" style="height:${pct}%;background:${color};"></div>
      </div>
      <div class="fd-val" style="color:${color};">${pct}</div>
      <div class="fd-level ${levelClass}">${day.demand_level}</div>
    `;
    grid.appendChild(el);
  });
}

function renderVendorTable(vendors) {
  const tbody = document.getElementById('vendorTableBody');
  if (!vendors || !vendors.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-light);">No vendors registered yet.</td></tr>';
    return;
  }
  tbody.innerHTML = vendors.map(v => `
    <tr>
      <td><strong>${escHtml(v.name)}</strong></td>
      <td>${escHtml(v.business_type)}</td>
      <td>${escHtml(v.location)}</td>
      <td>${v.upi_id ? `<span class="upi-badge upi-yes">Active</span>` : `<span class="upi-badge upi-no">None</span>`}</td>
      <td>${v.registered_at ? new Date(v.registered_at).toLocaleDateString() : '--'}</td>
    </tr>
  `).join('');
}

loadDashboard();
setInterval(loadDashboard, 30000);
