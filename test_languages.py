import urllib.request, json, ssl, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ctx = ssl.create_default_context()
RENDER = 'https://street-vendor-digitalization-agent-isog.onrender.com'

def post(endpoint, data):
    req = urllib.request.Request(
        RENDER + endpoint,
        data=json.dumps(data).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    resp = urllib.request.urlopen(req, timeout=120, context=ctx)
    return json.loads(resp.read().decode())

langs = {
    'en': ('English', range(0x41, 0x5B)),
    'hi': ('Hindi', range(0x0900, 0x097F)),
    'ta': ('Tamil', range(0x0B80, 0x0BFF)),
    'te': ('Telugu', range(0x0C00, 0x0C7F)),
    'mr': ('Marathi', range(0x0900, 0x097F)),
    'kn': ('Kannada', range(0x0C80, 0x0CFF)),
    'gu': ('Gujarati', range(0x0A80, 0x0AFF)),
    'bn': ('Bengali', range(0x0980, 0x09FF)),
}

print("=" * 60)
print("  LANGUAGE TEST: /api/query")
print("=" * 60)

for code, (name, char_range) in langs.items():
    result = post('/api/query', {"query": "How to set up UPI payment?", "language": code})
    answer = result['answer']
    has_script = any(ord(c) in char_range for c in answer) if code != 'en' else True
    first_line = answer.split('\n')[0][:100]
    print(f"\n  [{code}] {name}:")
    print(f"    First line: {first_line}")
    print(f"    Correct script: {'PASS' if has_script else 'FAIL - still English!'}")
    print(f"    Length: {len(answer)} chars")

print()
print("=" * 60)
print("  LANGUAGE TEST: /api/generate-kit")
print("=" * 60)

for code, (name, char_range) in langs.items():
    result = post('/api/generate-kit', {
        "vendor_name": "Ramesh",
        "business_type": "Fruit Vendor",
        "location": "Camp, Pune",
        "upi_id": "ramesh@upi",
        "language": code
    })
    answer = result['answer']
    has_script = any(ord(c) in char_range for c in answer) if code != 'en' else True
    first_line = answer.split('\n')[0][:100]
    print(f"\n  [{code}] {name}:")
    print(f"    First line: {first_line}")
    print(f"    Correct script: {'PASS' if has_script else 'FAIL - still English!'}")
    print(f"    Length: {len(answer)} chars")
