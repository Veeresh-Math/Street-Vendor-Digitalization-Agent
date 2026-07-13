/* vendor-map.js — Leaflet.js interactive vendor map */

let vendorMap = null;
let vendorMarkers = [];

function escHtmlMap(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
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

function initVendorMap() {
  const mapEl = document.getElementById('vendorMap');
  if (!mapEl || vendorMap) return;

  // Default center: India
  vendorMap = L.map('vendorMap', {
    zoomControl: true,
    scrollWheelZoom: false,
  }).setView([20.5937, 78.9629], 5);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18,
  }).addTo(vendorMap);

  loadVendors();

  // If user location available, fly to it
  if (userLocation && userLocation.lat && userLocation.lon) {
    vendorMap.setView([userLocation.lat, userLocation.lon], 12);
  }
}

async function loadVendors() {
  try {
    const apiBase = window.location.origin || '';
    const res = await fetch(`${apiBase}/api/vendors`);
    if (!res.ok) return;
    const vendors = await res.json();

    vendors.forEach(v => {
      if (!v.lat || !v.lon) return;
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
          <div style="font-weight:800;font-size:14px;color:#1B2A6B;margin-bottom:4px;">${escHtmlMap(v.name)}</div>
          <div style="font-size:12px;color:#5C5040;margin-bottom:4px;">${escHtmlMap(v.business_type)}</div>
          <div style="font-size:11px;color:#8B7355;">📍 ${escHtmlMap(v.location)}</div>
          ${v.upi_id ? `<div style="font-size:11px;color:#2D6A4F;margin-top:4px;">💳 ${escHtmlMap(v.upi_id)}</div>` : ''}
        </div>
      `;
      marker.bindPopup(popupHtml);
      vendorMarkers.push({ marker, vendor: v });
    });
  } catch (e) {
    console.warn('Failed to load vendors for map:', e);
  }
}

// Auto-init on agent page
if (document.getElementById('vendorMap')) {
  if (typeof L !== 'undefined') {
    initVendorMap();
  } else {
    window.addEventListener('load', initVendorMap);
  }
}
