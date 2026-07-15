import urllib.request, json, ssl, sys, io, time, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = 'http://127.0.0.1:8000'
PASS = 0
FAIL = 0
TOTAL = 0

def post(endpoint, data):
    req = urllib.request.Request(BASE + endpoint, data=json.dumps(data).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode())

def get(endpoint):
    req = urllib.request.Request(BASE + endpoint)
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())

def check(name, condition, detail=""):
    global PASS, FAIL, TOTAL
    TOTAL += 1
    if condition:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name} {detail}")

# ═══════════════════════════════════════════════════
# PHASE 1: NO-TOKEN ENDPOINTS (free tests)
# ═══════════════════════════════════════════════════
print("=" * 55)
print("  PHASE 1: NO-TOKEN ENDPOINTS")
print("=" * 55)

# Ping
try:
    r = get('/api/ping')
    check('GET /api/ping', r.get('status') == 'ok')
except Exception as e:
    check('GET /api/ping', False, str(e))

# Vendors
try:
    r = get('/api/vendors')
    check('GET /api/vendors', isinstance(r, list) and len(r) >= 10, f"got {len(r)}")
except Exception as e:
    check('GET /api/vendors', False, str(e))

# Analytics
try:
    r = get('/api/analytics')
    check('GET /api/analytics', isinstance(r, dict) and 'total_vendors' in r)
except Exception as e:
    check('GET /api/analytics', False, str(e))

# Schemes (may not exist)
try:
    r = get('/api/schemes')
    check('GET /api/schemes', isinstance(r, list))
except:
    check('GET /api/schemes', False, "(endpoint may not exist)")

# QR
try:
    r = post('/api/qr', {"upi_id": "test@upi", "vendor_name": "Test"})
    qr = r.get('qr_url', '')
    check('POST /api/qr', bool(qr), qr)
    if qr:
        path = os.path.join('static', qr.lstrip('/static/'))
        check('QR file on disk', os.path.exists(path))
except Exception as e:
    check('POST /api/qr', False, str(e))

# Forecast (check correct method)
try:
    r = post('/api/forecast', {"location": "Pune", "business_type": "Fruit Vendor"})
    check('POST /api/forecast', isinstance(r, dict) and len(r) > 0)
except Exception as e:
    check('POST /api/forecast', False, str(e))

# Frontend pages
for page in ['/', '/agent', '/dashboard']:
    try:
        req = urllib.request.Request(BASE + page)
        resp = urllib.request.urlopen(req, timeout=10)
        check(f'GET {page}', resp.status == 200)
    except Exception as e:
        check(f'GET {page}', False, str(e))

# ═══════════════════════════════════════════════════
# PHASE 2: LLM ENDPOINTS (token cost - minimal)
# ═══════════════════════════════════════════════════
print()
print("=" * 55)
print("  PHASE 2: LLM ENDPOINTS (minimal tokens)")
print("=" * 55)

# Patch max_tokens for testing by overriding in the call
# We'll modify the query to use top_k=1 and shorter prompts

# Test 1 query - English
try:
    t0 = time.time()
    r = post('/api/query', {"query": "UPI setup", "language": "en", "top_k": 1})
    elapsed = time.time() - t0
    check('Query [en] English', bool(r.get('answer')) and len(r['answer']) > 20, f"{elapsed:.1f}s, {len(r.get('answer',''))} chars")
except Exception as e:
    check('Query [en] English', False, str(e))

# Test 1 kit - English
try:
    t0 = time.time()
    r = post('/api/generate-kit', {"vendor_name": "Test", "business_type": "Tea", "location": "Pune", "upi_id": "test@upi", "language": "en"})
    elapsed = time.time() - t0
    check('Kit [en] English', bool(r.get('answer')) and bool(r.get('qr_url')), f"{elapsed:.1f}s")
except Exception as e:
    check('Kit [en] English', False, str(e))

# Test 1 query each remaining language (top_k=1 to save tokens)
lang_ranges = {
    'hi': ('Hindi',    range(0x0900, 0x097F)),
    'mr': ('Marathi',  range(0x0900, 0x097F)),
    'ta': ('Tamil',    range(0x0B80, 0x0BFF)),
    'te': ('Telugu',   range(0x0C00, 0x0C7F)),
    'kn': ('Kannada',  range(0x0C80, 0x0CFF)),
    'gu': ('Gujarati', range(0x0A80, 0x0AFF)),
    'bn': ('Bengali',  range(0x0980, 0x09FF)),
}

for code, (name, cr) in lang_ranges.items():
    try:
        t0 = time.time()
        r = post('/api/query', {"query": "UPI setup", "language": code, "top_k": 1})
        elapsed = time.time() - t0
        ans = r.get('answer', '')
        has = any(c in cr for c in ans)
        check(f'Query [{code}] {name}', has and len(ans) > 20, f"{elapsed:.1f}s, script_ok={has}")
    except Exception as e:
        check(f'Query [{code}] {name}', False, str(e))

# Test kit for Tamil and Bengali (the previously failing ones)
for code in ['ta', 'bn']:
    name = lang_ranges[code][0]
    try:
        t0 = time.time()
        r = post('/api/generate-kit', {"vendor_name": "Ramesh", "business_type": "Fruit", "location": "Pune", "upi_id": "r@upi", "language": code})
        elapsed = time.time() - t0
        ans = r.get('answer', '')
        cr = lang_ranges[code][1]
        has = any(c in cr for c in ans)
        check(f'Kit [{code}] {name}', has and len(ans) > 20, f"{elapsed:.1f}s, script_ok={has}")
    except Exception as e:
        check(f'Kit [{code}] {name}', False, str(e))

# ═══════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════
print()
print("=" * 55)
print(f"  RESULTS: {PASS}/{TOTAL} PASS, {FAIL} FAIL")
print("=" * 55)
