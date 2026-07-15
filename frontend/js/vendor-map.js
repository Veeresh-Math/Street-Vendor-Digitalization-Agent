/* vendor-map.js — Leaflet.js interactive vendor map with city/type filtering */

let vendorMap = null;
let vendorMarkers = [];
let allVendors = [];
let activeFilter = { city: 'all', type: 'all' };

function escHtml(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

const VENDOR_COLORS = {
  'Fruit & Vegetable Vendor': '#2D6A4F',
  'Vegetable Vendor': '#2D6A4F',
  'South Indian Food Stall': '#D7263D',
  'Street Food Stall': '#D7263D',
  'Chaat & Snacks': '#D7263D',
  'Biryani & Rice Stall': '#D7263D',
  'Saree & Clothing Vendor': '#1B2A6B',
  'Textile & Accessories': '#1B2A6B',
  'Flower Vendor': '#F5A623',
  'Electronics Repair Shop': '#6366f1',
};

function getMarkerColor(businessType) {
  for (const [key, color] of Object.entries(VENDOR_COLORS)) {
    if (businessType.toLowerCase().includes(key.toLowerCase())) return color;
  }
  return '#1B2A6B';
}

function getCityFromLocation(location) {
  if (!location) return '';
  const parts = location.split(',').map(s => s.trim());
  return parts[parts.length - 1] || '';
}

function buildFilterUI() {
  const container = document.getElementById('vendorMap');
  if (!container) return;

  const filterBar = document.createElement('div');
  filterBar.id = 'mapFilterBar';
  filterBar.style.cssText = 'display:flex;gap:8px;padding:8px 10px;flex-wrap:wrap;align-items:center;background:rgba(255,255,255,0.02);border-bottom:1px solid rgba(255,255,255,0.06);';

  filterBar.innerHTML = `
    <span style="font-size:11px;color:rgba(255,255,255,0.56);font-weight:600;">Filter:</span>
    <select id="mapCityFilter" style="padding:4px 8px;border-radius:6px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.04);color:rgba(255,255,255,0.91);font-size:11px;">
      <option value="all">All Cities</option>
    </select>
    <select id="mapTypeFilter" style="padding:4px 8px;border-radius:6px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.04);color:rgba(255,255,255,0.91);font-size:11px;">
      <option value="all">All Types</option>
    </select>
    <span id="mapVendorCount" style="font-size:10px;color:rgba(255,255,255,0.30);margin-left:auto;"></span>
  `;

  container.parentNode.insertBefore(filterBar, container);
}

function populateFilters(vendors) {
  const validVendors = vendors.filter(v => v.lat != null && v.lon != null);
  const cities = [...new Set(validVendors.map(v => v.city || getCityFromLocation(v.location)).filter(Boolean))].sort();
  const types = [...new Set(validVendors.map(v => v.business_type).filter(Boolean))].sort();

  const citySelect = document.getElementById('mapCityFilter');
  const typeSelect = document.getElementById('mapTypeFilter');
  if (!citySelect || !typeSelect) return;

  cities.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c; opt.textContent = c;
    citySelect.appendChild(opt);
  });
  types.forEach(t => {
    const opt = document.createElement('option');
    opt.value = t; opt.textContent = t;
    typeSelect.appendChild(opt);
  });

  if (window.__USER_CITY__) {
    citySelect.value = window.__USER_CITY__;
    activeFilter.city = window.__USER_CITY__;
  }

  citySelect.addEventListener('change', () => { activeFilter.city = citySelect.value; applyFilters(); });
  typeSelect.addEventListener('change', () => { activeFilter.type = typeSelect.value; applyFilters(); });
}

function applyFilters() {
  const filtered = allVendors.filter(v => {
    if (v.lat == null || v.lon == null) return false;
    const city = v.city || getCityFromLocation(v.location);
    const matchCity = activeFilter.city === 'all' || city === activeFilter.city;
    const matchType = activeFilter.type === 'all' || v.business_type === activeFilter.type;
    return matchCity && matchType;
  });

  vendorMarkers.forEach(m => vendorMap.removeLayer(m.marker));
  vendorMarkers = [];

  filtered.forEach(v => {
    const color = getMarkerColor(v.business_type || '');
    const marker = L.circleMarker([v.lat, v.lon], {
      radius: 8,
      fillColor: color,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.85,
    }).addTo(vendorMap);

    const popupHtml = `
      <div style="font-family:system-ui;min-width:180px;">
        <div style="font-weight:800;font-size:14px;color:#1B2A6B;margin-bottom:4px;">${escHtml(v.name)}</div>
        <div style="font-size:12px;color:#5C5040;margin-bottom:4px;">${escHtml(v.business_type)}</div>
        <div style="font-size:11px;color:#8B7355;">📍 ${escHtml(v.location)}</div>
        ${v.upi_id ? `<div style="font-size:11px;color:#2D6A4F;margin-top:4px;">💳 ${escHtml(v.upi_id)}</div>` : ''}
      </div>
    `;
    marker.bindPopup(popupHtml);
    vendorMarkers.push({ marker, vendor: v });
  });

  const countEl = document.getElementById('mapVendorCount');
  if (countEl) countEl.textContent = `${filtered.length} of ${allVendors.length} vendors`;

  if (filtered.length > 0) {
    const bounds = L.latLngBounds(filtered.map(v => [v.lat, v.lon]));
    vendorMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 12, animate: true });
  }
}

function initVendorMap() {
  const mapEl = document.getElementById('vendorMap');
  if (!mapEl || vendorMap) return;

  vendorMap = L.map('vendorMap', {
    zoomControl: true,
    scrollWheelZoom: false,
    attributionControl: true,
    maxBoundsViscosity: 0.8,
  }).setView([20.5937, 78.9629], 5);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18,
  }).addTo(vendorMap);

  buildFilterUI();
  loadVendors();

  if (window.userLocation && window.userLocation.lat && window.userLocation.lon) {
    vendorMap.setView([window.userLocation.lat, window.userLocation.lon], 12);
  }

  setTimeout(() => vendorMap.invalidateSize(), 300);
}

async function loadVendors() {
  try {
    const apiBase = window.__API_BASE__ || window.location.origin || '';
    const res = await fetch(`${apiBase}/api/vendors`);
    if (!res.ok) return;
    allVendors = await res.json();

    populateFilters(allVendors);
    applyFilters();
  } catch (e) {
    console.warn('Failed to load vendors for map:', e);
  }
}

if (document.getElementById('vendorMap')) {
  if (typeof L !== 'undefined') {
    initVendorMap();
  } else {
    window.addEventListener('load', initVendorMap);
  }
}
