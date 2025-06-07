import subprocess
import sys

if sys.platform != "win32": 
    result = subprocess.run(['ls','-la'], capture_output=True, text=True, check=False)
    print(f"\n-- 'ls -la' output (first 100 chars): ---\n{result.stdout[:100]}...")
    print(f"Return code: {result.returncode}")
else: 
    print("Skipping 'ls -la' on windows for this example.")
