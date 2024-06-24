# Description:

Super simple utility to return the output of `scontrol show` parsed. 

**Example:**

Print a table with the info of a few jobs:
```python
import scontrol_parser

job_ids = [12232, 31231, 32123]

job_id_to_info = {job_id: scontrol_parser.call(job_id) for job_id in job_ids}

for job_id, info in job_id_to_info.items():
  print(f"job_id: {job_id}")
  for key, value in info.items()
    print(f"{key}: {value}")
  print()
```

Find out if the current job was launched with `sbatch`:
```python

import scontrol_parser

batch_flag = scontrol_parser.call()["BatchFlag"]

if batch_flag == "1":
  print("Called with sbatch")
else:
  print("Interactive or Srun")
  
```
