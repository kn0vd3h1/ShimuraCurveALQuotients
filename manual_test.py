import subprocess
import os

# Simulate matrix job
cmd_matrix = r"""
matrix=$( (
  echo '{ "target" : ['
  ls -1 tests | grep -v '^_' | sed -r 's/^([^,]*)(,?)$/"\1"\2/'  | paste -sd "," -
  echo " ]}"
) | jq -c .)
echo "$matrix"
"""
matrix_output = subprocess.check_output(["/bin/bash", "-c", cmd_matrix], text=True).strip()
print("MATRIX:", matrix_output)

# Simulate check-matrix job
os.environ["GITHUB_RUN_ID"] = "12345"
cmd_check = f"matrix='{matrix_output}'"
# Run with bash -x to see what's happening
result = subprocess.run(["/bin/bash", "-xc", cmd_check], capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
