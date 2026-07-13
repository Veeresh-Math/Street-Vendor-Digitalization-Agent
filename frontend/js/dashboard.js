/* dashboard.js — Dashboard analytics and charts */

const apiBase = window.__API_BASE__ || window.location.origin || '';

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
      document.getElementById('statTotal').textContent = stats.total_vendors;
      document.getElementById('statUpi').textContent = stats.vendors_with_upi;
      document.getElementById('statCities').textContent = Object.keys(stats.city_counts).length;
      document.getElementById('statBiz').textContent = Object.keys(stats.business_counts).length;

      renderCityChart(stats.city_counts);
      renderBizChart(stats.business_counts);
      renderVendorTable(stats.recent_vendors);
    }

    if (forecastRes.ok) {
      const forecast = await forecastRes.json();
      renderForecast(forecast);
    }
  } catch (e) {
    console.error('Dashboard load error:', e);
  }
}

function renderCityChart(cityCounts) {
  const ctx = document.getElementById('cityChart');
  if (!ctx) return;
  const labels = Object.keys(cityCounts);
  const data = Object.values(cityCounts);
  const colors = ['#FF6B00', '#F5C518', '#1A7A4A', '#FF5733', '#38bdf8', '#818cf8'];

  new Chart(ctx, {
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
}

function renderBizChart(bizCounts) {
  const ctx = document.getElementById('bizChart');
  if (!ctx) return;
  const labels = Object.keys(bizCounts);
  const data = Object.values(bizCounts);
  const colors = ['#FF6B00', '#F5C518', '#1A7A4A', '#FF5733', '#38bdf8', '#818cf8', '#ec4899'];

  new Chart(ctx, {
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
