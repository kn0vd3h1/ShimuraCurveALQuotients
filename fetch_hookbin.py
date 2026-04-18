import json
import urllib.request
import sys

bin_id = sys.argv[1]
url = f"https://open-hookbin.vercel.app/api/{bin_id}"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
    print(json.dumps(data, indent=2))
