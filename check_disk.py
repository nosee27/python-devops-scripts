#!/usr/bin/env python3
import subprocess
from datetime import datetime
try:
    result=subprocess.run(
            ["df","-h"],
            capture_output=True,
            text=True,
            )
    print(result.stdout)
    print(f"[{datetime.now()}]",end=" ")
except Exception as e:
    print({e})
