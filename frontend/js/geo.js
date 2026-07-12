/* geo.js — Optional geolocation via browser + /api/geocode */

let userLocation = null;

async function detectLocation() {
  if (!navigator.geolocation) return;
  navigator.geolocation.getCurrentPosition(async pos => {
    const { latitude: lat, longitude: lon } = pos.coords;
    try {
      // Reverse geocode via Nominatim through our backend
      const r = await fetch(`https://street-vendor-digitalization-agent-isog.onrender.com/api/geocode?q=${lat},${lon}`);
      const d = await r.json();
      if (d.found) {
        userLocation = d;
        const locField = document.getElementById('fLocation');
        if (locField && !locField.value) {
          locField.value = d.locality
            ? `${d.locality}, ${d.city}`
            : d.city || d.display_name?.split(',')[0] || '';
        }
      }
    } catch(e) { /* silent */ }
  }, () => { /* permission denied — silent */ });
}

// Auto-detect on agent page load
detectLocation();

