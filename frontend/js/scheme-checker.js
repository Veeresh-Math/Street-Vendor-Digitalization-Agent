/* scheme-checker.js — PM SVANidhi eligibility via backend API */

async function checkScheme(el, answer) {
  el.parentElement.querySelectorAll('.scheme-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');

  const resultEl = document.getElementById('schemeResult');
  resultEl.style.display = 'block';
  resultEl.innerHTML = 'Checking eligibility...';

  const hasCov = (answer === 'yes');
  const hasLor = (answer === 'lor');
  const isFood = (answer === 'food_yes');
  const city = document.getElementById('fLocation')?.value || '';

  try {
    const apiBase = window.location.origin || '';
    const res = await fetch(`${apiBase}/api/scheme-check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ has_cov: hasCov, has_lor: hasLor, is_food_vendor: isFood, city }),
    });
    const data = await res.json();

    let html = '<strong>Based on your profile:</strong><br/><br/>';
    if (data.eligible) {
      data.schemes.forEach(s => {
        const icon = s.eligible ? '✅' : '❌';
        html += `<strong>${s.name}:</strong> ${s.amount} ${icon}<br/>`;
        if (s.eligible) html += `<span style="font-size:11px;color:var(--text-light);">${s.benefit}</span><br/>`;
        html += '<br/>';
      });
      html += '<strong>Documents needed:</strong><br/>';
      data.documents_needed.forEach(d => { html += `• ${d}<br/>`; });
      html += '<br/><strong>Next steps:</strong><br/>';
      data.next_steps.forEach(s => { html += `• ${s}<br/>`; });
    } else {
      html += '<strong>Not yet eligible for PM SVANidhi.</strong><br/>';
      html += 'You need a Certificate of Vending (CoV) or Letter of Recommendation (LoR).<br/><br/>';
      html += '<strong>What you can do now:</strong><br/>';
      data.next_steps.forEach(s => { html += `• ${s}<br/>`; });
      html += '<br/>You can still register for MSME Udyam (free) and e-Shram card.';
    }

    html += '<div style="margin-top:10px;"><button class="scheme-opt" onclick="resetScheme()" style="background:var(--indigo);color:#fff;">Check Again</button></div>';
    resultEl.innerHTML = html;
  } catch (e) {
    resultEl.innerHTML = 'Error checking eligibility. Please try again.';
  }
}

function resetScheme() {
  const resultEl = document.getElementById('schemeResult');
  resultEl.style.display = 'none';
  resultEl.innerHTML = '';
  document.querySelectorAll('.scheme-opt').forEach(o => o.classList.remove('selected'));
}
